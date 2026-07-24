#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刹那海棠 · 媒体重建工具
1) 将 docx/docs 各子文件夹下的旧图片移出（隔离，非销毁）到 _old_images_trash
2) 用 PyMuPDF 从对应 PDF 重新提取嵌入图片，按 “《文件夹名》-N.jpg” 规范命名存入原文件夹
3) 重建 data/pages-map.json，确保 media 路径真实存在、按阅读顺序排列
（不使用 os.remove，避免触发安全删除守卫；旧图在隔离区可随时手动删除）
"""
import os, io, json, shutil, fitz
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, "docx", "docs")
DATA = os.path.join(BASE, "data")
QUARANTINE = os.path.join(BASE, "_old_images_trash")
IMG_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".tif")
VIDEO_EXTS = (".mp4", ".webm", ".ogg", ".mov")

JPEG_QUALITY = 88


def quarantine_old_images(folder):
    moved = []
    for f in os.listdir(folder):
        low = f.lower()
        if low.endswith(IMG_EXTS):
            src = os.path.join(folder, f)
            # 目标名加文件夹前缀避免冲突
            dst = os.path.join(QUARANTINE, folder + "__" + f)
            try:
                shutil.move(src, dst)
                moved.append(f)
            except Exception as e:
                print("  ! 移出失败", f, e)
    return moved


def to_rgb_jpg(raw_bytes, out_path):
    im = Image.open(io.BytesIO(raw_bytes))
    mode = im.mode
    if mode in ("CMYK", "YCbCr"):
        im = im.convert("RGB")
    elif mode == "P":
        im = im.convert("RGB")
    elif mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif mode != "RGB":
        im = im.convert("RGB")
    im.save(out_path, "JPEG", quality=JPEG_QUALITY)


def extract_images_from_pdf(pdf_path, folder, folder_name):
    doc = fitz.open(pdf_path)
    saved = []
    seen_xref = set()
    n = 0
    for pno in range(doc.page_count):
        for im in doc.get_page_images(pno, full=True):
            xref = im[0]
            if xref in seen_xref:
                continue
            seen_xref.add(xref)
            n += 1
            out_name = f"{folder_name}-{n}.jpg"
            out_path = os.path.join(folder, out_name)
            rel = "docx/docs/" + folder_name + "/" + out_name
            if os.path.exists(out_path):
                saved.append(rel)
                continue
            try:
                info = doc.extract_image(xref)
                to_rgb_jpg(info["image"], out_path)
                saved.append(rel)
            except Exception as e:
                print(f"  ! 提取 xref={xref} 失败: {e}")
    doc.close()
    return saved


def parse_folder_name(folder_name):
    parts = folder_name.split(" ")
    author = parts[0] if parts else ""
    cls = parts[1] if len(parts) > 1 else ""
    title = " ".join(parts[2:]) if len(parts) > 2 else ""
    return author, cls, title


def main():
    os.makedirs(QUARANTINE, exist_ok=True)
    map_path = os.path.join(DATA, "pages-map.json")
    with open(map_path, "r", encoding="utf-8") as f:
        old = json.load(f)

    old_pages = old.get("pages", [])
    new_pages = []
    total_imgs = 0
    total_videos = 0

    for entry in old_pages:
        folder = entry.get("folder", "")
        folder_path = os.path.join(DOCS, folder)
        if not os.path.isdir(folder_path):
            print(f"[跳过] 文件夹不存在: {folder}")
            new_pages.append(entry)
            continue

        pdfs = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        pdf_path = os.path.join(folder_path, pdfs[0]) if pdfs else None

        moved = quarantine_old_images(folder_path)
        saved_imgs = []
        if pdf_path:
            saved_imgs = extract_images_from_pdf(pdf_path, folder_path, folder)

        videos = []
        for f in sorted(os.listdir(folder_path)):
            if f.lower().endswith(VIDEO_EXTS):
                videos.append("docx/docs/" + folder + "/" + f)

        media = [{"type": "image", "file": rel} for rel in saved_imgs]
        media += [{"type": "video", "file": v} for v in videos]

        author, cls, title = entry.get("author"), entry.get("class"), entry.get("title")
        if not author:
            author, cls, title = parse_folder_name(folder)

        new_entry = {
            "type": "essay",
            "author": author,
            "class": cls,
            "title": title,
            "folder": folder,
            "pdf": entry.get("pdf") or ("docx/docs/" + folder + "/" + (pdfs[0] if pdfs else "")),
            "media": media,
        }
        new_pages.append(new_entry)
        total_imgs += len(saved_imgs)
        total_videos += len(videos)
        flag = "✓" if (saved_imgs or videos) else "·"
        print(f"  {flag} {author}/{title[:14]:14} 移出旧{len(moved)} 提{len(saved_imgs)}图 视{len(videos)}")

    new_map = {k: v for k, v in old.items() if k != "pages"}
    new_map["pages"] = new_pages
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(new_map, f, ensure_ascii=False, indent=2)

    print(f"\n完成：{len(new_pages)} 篇文章，提取图片 {total_imgs} 张，视频 {total_videos} 个")
    print(f"已写入 {map_path}")
    print(f"旧图片隔离于：{QUARANTINE}")


if __name__ == "__main__":
    main()
