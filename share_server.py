#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
局域网文件共享服务器
使用方法：
1. 运行此脚本：python share_server.py
2. 在局域网内的其他设备上访问显示的URL
3. 可以通过浏览器访问共享的文件

可选参数：
  -p, --port    指定端口号（默认8000）
  -d, --dir     指定共享目录（默认为当前目录）
"""

import os
import sys
import argparse
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_local_ips():
    """获取本机所有局域网IP地址"""
    ips = []
    try:
        hostname = socket.gethostname()
        # 获取所有IP地址
        addresses = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for addr in addresses:
            ip = addr[4][0]
            # 过滤掉回环地址和IPv6地址
            if ip != '127.0.0.1' and not ip.startswith('169.254'):
                ips.append(ip)
        # 如果没有找到，尝试另一种方法
        if not ips:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ips.append(s.getsockname()[0])
            s.close()
    except Exception as e:
        print(f"获取IP地址时出错: {e}")
    return ips


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='局域网文件共享服务器')
    parser.add_argument('-p', '--port', type=int, default=8000, 
                        help='指定服务端口（默认8000）')
    parser.add_argument('-d', '--dir', type=str, default='.', 
                        help='指定共享目录（默认为当前目录）')
    args = parser.parse_args()
    
    # 设置工作目录
    share_dir = os.path.abspath(args.dir)
    if not os.path.isdir(share_dir):
        print(f"错误：目录 '{share_dir}' 不存在")
        sys.exit(1)
    
    os.chdir(share_dir)
    
    # 获取本机IP地址
    local_ips = get_local_ips()
    
    # 创建HTTP服务器
    server_address = ('0.0.0.0', args.port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    # 打印服务器信息
    print("=" * 60)
    print("局域网文件共享服务器已启动")
    print("=" * 60)
    print(f"共享目录: {share_dir}")
    print(f"服务端口: {args.port}")
    print("\n局域网访问地址:")
    for ip in local_ips:
        print(f"  http://{ip}:{args.port}")
    print(f"  http://localhost:{args.port} (本机访问)")
    print("\n按 Ctrl+C 停止服务")
    print("=" * 60)
    
    try:
        # 启动服务器
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        httpd.server_close()
        sys.exit(0)


if __name__ == "__main__":
    main()