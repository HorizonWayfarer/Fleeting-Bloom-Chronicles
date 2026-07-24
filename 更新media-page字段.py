#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只更新 data/pages-map.json：给每个 image media 补上 page(来自PDF第几页,1based)
与 bbox(该图在PDF页上的精确包围盒 [x0,y0,x1,y1]，PyMuPDF 坐标系：左上原点、y向下、单位pt)。
不移动、不重命名、不重新提取任何图片，安全可重复运行。
前端将用 bbox 直接定位热点（地面真相），不再依赖 PDF.js 的绘制指令回放检测。
视频无 bbox，前端会回退到检测/角落兜底。
"""
import os, json, fitz

BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, "docx", "docs")
DATA = os.path.join(BASE, "data")
MAP = os.path.join(DATA, "pages-map.json")


def per_page_info(pdf_path):
    """返回 (order[(xref,page1)], bbox_by_xref, npages)"""
    doc = fitz.open(pdf_path)
    order = []
    seen = set()
    bbox_by_xref = {}
    for pno in range(doc.page_count):
        for im in doc.get_page_images(pno, full=True):
            xr = im[0]
            if xr in seen:
                continue
            seen.add(xr)
            order.append((xr, pno + 1))
        # 收集本页图片 bbox（按 xref）
        for it in doc[pno].get_image_info(xrefs=True):
            xr = it.get("xref")
            bbox = it.get("bbox")
            if xr is not None and bbox is not None:
                bbox_by_xref[xr] = [round(float(v), 1) for v in bbox]
    npages = doc.page_count
    doc.close()
    return order, bbox_by_xref, npages


def main():
    m = json.load(open(MAP, encoding="utf-8"))
    for e in m.get("pages", []):
        folder = e.get("folder", "")
        fp = os.path.join(DOCS, folder)
        pdfs = [f for f in os.listdir(fp) if f.lower().endswith(".pdf")] if os.path.isdir(fp) else []
        pdf_path = os.path.join(fp, pdfs[0]) if pdfs else None

        order, bbox_by_xref, npages = ([], {}, 1)
        if pdf_path and os.path.exists(pdf_path):
            order, bbox_by_xref, npages = per_page_info(pdf_path)

        img_idx = 0
        media = e.get("media", [])
        for md in media:
            if md.get("type") == "video":
                md["page"] = npages
                md.pop("bbox", None)  # 视频无 bbox
            else:
                md["page"] = order[img_idx][1] if img_idx < len(order) else 1
                xr = order[img_idx][0] if img_idx < len(order) else None
                md["bbox"] = bbox_by_xref.get(xr)  # 可能为 None（极端情况）
                img_idx += 1
        e["media"] = media

    json.dump(m, open(MAP, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("已更新", MAP, "（含 page + bbox）")


if __name__ == "__main__":
    main()
