#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态生成杂志图片映射和缩略图HTML
使用方法：
1. 创建一个 images.txt 文件，每行一个图片文件名
2. 运行此脚本：python generate_magazine.py
3. 脚本会自动更新 js/magazine.js 和 index.html
"""

import os

def read_image_files(txt_path):
    """从txt文件读取图片文件名"""
    # 尝试不同的编码
    encodings = ['utf-8', 'gbk', 'gb2312']
    for encoding in encodings:
        try:
            with open(txt_path, 'r', encoding=encoding) as f:
                images = [line.strip() for line in f if line.strip()]
            return images
        except UnicodeDecodeError:
            continue
    # 如果所有编码都失败，返回空列表
    print("无法读取images.txt文件，请检查文件编码")
    return []

def generate_js_array(images):
    """生成JavaScript数组字符串"""
    lines = ["// 图片文件名映射", "var imageFiles = ["]
    for img in images:
        lines.append(f'    "{img}",')
    lines.append("];")
    return '\n'.join(lines)

def generate_thumbnails_html(images):
    """生成缩略图HTML"""
    lines = ["\t\t\t<ul>"]
    page_num = 1
    total_pages = len(images)
    
    # 处理封面页（第一页）
    lines.append('\t\t\t\t<li class="i">')
    lines.append(f'\t\t\t\t\t<img src="pages/thumb/{images[0]}" width="76" height="100" class="page-{page_num}">')
    lines.append(f'\t\t\t\t\t<span>{page_num}</span>')
    lines.append('\t\t\t\t</li>')
    page_num += 1
    
    # 计算中间内容页数（抛去封面和封尾）
    middle_pages = total_pages - 2
    # 检查中间内容页数是否为奇数
    middle_is_odd = middle_pages % 2 == 1
    
    # 处理中间页
    while page_num < total_pages:
        # 如果中间内容页数是奇数，并且当前是倒数第二页（最后一个内容页），那么和封尾组成双页
        if middle_is_odd and page_num == total_pages - 1:
            # 最后一个内容页和封尾组成双页
            lines.append('\t\t\t\t<li class="d">')
            lines.append(f'\t\t\t\t\t<img src="pages/thumb/{images[page_num-1]}" width="76" height="100" class="page-{page_num}">')
            lines.append(f'\t\t\t\t\t<img src="pages/thumb/{images[page_num]}" width="76" height="100" class="page-{page_num+1}">')
            lines.append(f'\t\t\t\t\t<span>{page_num}-{page_num+1}</span>')
            lines.append('\t\t\t\t</li>')
            page_num += 2
        elif page_num == total_pages - 1:
            # 中间内容页数是偶数，封尾单独一页
            lines.append('\t\t\t\t<li class="i">')
            lines.append(f'\t\t\t\t\t<img src="pages/thumb/{images[page_num-1]}" width="76" height="100" class="page-{page_num}">')
            lines.append(f'\t\t\t\t\t<span>{page_num}</span>')
            lines.append('\t\t\t\t</li>')
            page_num += 1
        else:
            # 正常双页
            lines.append('\t\t\t\t<li class="d">')
            lines.append(f'\t\t\t\t\t<img src="pages/thumb/{images[page_num-1]}" width="76" height="100" class="page-{page_num}">')
            lines.append(f'\t\t\t\t\t<img src="pages/thumb/{images[page_num]}" width="76" height="100" class="page-{page_num+1}">')
            lines.append(f'\t\t\t\t\t<span>{page_num}-{page_num+1}</span>')
            lines.append('\t\t\t\t</li>')
            page_num += 2
    
    lines.append("\t\t\t</ul>")
    return '\n'.join(lines)

def update_js_file(js_path, new_content):
    """更新JavaScript文件"""
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换imageFiles数组
    start_marker = "// 图片文件名映射"
    end_marker = "];"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("未找到imageFiles数组开始标记")
        return False
    
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("未找到imageFiles数组结束标记")
        return False
    
    end_idx += len(end_marker)
    new_js_content = content[:start_idx] + new_content + content[end_idx:]
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(new_js_content)
    
    return True

def update_html_file(html_path, new_thumbnails, total_pages):
    """更新HTML文件"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换缩略图部分
    start_marker = "\t\t\t<ul>"
    end_marker = "\t\t\t</ul>"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("未找到缩略图开始标记")
        return False
    
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("未找到缩略图结束标记")
        return False
    
    end_idx += len(end_marker)
    new_html_content = content[:start_idx] + new_thumbnails + content[end_idx:]
    
    # 替换pages值
    pages_marker = "pages: "
    pages_idx = new_html_content.find(pages_marker)
    if pages_idx != -1:
        # 找到pages值的位置
        end_pages_idx = new_html_content.find(",", pages_idx)
        if end_pages_idx != -1:
            # 替换pages值
            new_html_content = (new_html_content[:pages_idx + len(pages_marker)] + 
                               str(total_pages) + 
                               new_html_content[end_pages_idx:])
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    
    return True

def main():
    """主函数"""
    # 文件路径
    txt_path = "images.txt"
    js_path = "js/magazine.js"
    html_path = "index.html"
    
    # 检查文件是否存在
    if not os.path.exists(txt_path):
        print(f"错误：{txt_path} 文件不存在")
        print("请创建一个 images.txt 文件，每行一个图片文件名")
        return
    
    if not os.path.exists(js_path):
        print(f"错误：{js_path} 文件不存在")
        return
    
    if not os.path.exists(html_path):
        print(f"错误：{html_path} 文件不存在")
        return
    
    # 读取图片文件名
    images = read_image_files(txt_path)
    if not images:
        print("错误：images.txt 文件为空")
        return
    
    print(f"读取到 {len(images)} 个图片文件")
    
    # 生成JavaScript数组
    js_array = generate_js_array(images)
    
    # 生成缩略图HTML
    thumbnails_html = generate_thumbnails_html(images)
    
    # 更新文件
    js_updated = update_js_file(js_path, js_array)
    html_updated = update_html_file(html_path, thumbnails_html, len(images))
    
    if js_updated and html_updated:
        print("成功更新文件！")
        print(f"- 更新了 {js_path}")
        print(f"- 更新了 {html_path}")
        print(f"- 总页数：{len(images)}")
    else:
        print("更新失败")

if __name__ == "__main__":
    main()
