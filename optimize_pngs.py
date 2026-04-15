#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程 PNG 图片优化工具
使用 optipng 批量优化所有 PNG 文件
"""

import os
import threading
import queue
import subprocess
import sys

class PngOptimizer:
    def __init__(self, optipng_path, root_dir, max_threads=4):
        """初始化优化器"""
        self.optipng_path = optipng_path
        self.root_dir = root_dir
        self.max_threads = max_threads
        self.file_queue = queue.Queue()
        self.total_files = 0
        self.processed_files = 0
        self.lock = threading.Lock()
        
    def find_png_files(self):
        """查找所有 PNG 文件"""
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    file_path = os.path.join(root, file)
                    self.file_queue.put(file_path)
                    self.total_files += 1
        
    def optimize_png(self, thread_id):
        """优化单个 PNG 文件"""
        while not self.file_queue.empty():
            try:
                file_path = self.file_queue.get(block=False)
                
                # 构建 optipng 命令
                cmd = [
                    self.optipng_path,
                    '-o', '7',  # 最高优化级别
                    '-i', '1',  # 交织（渐进式加载）
                    file_path
                ]
                
                # 执行命令
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # 解析输出，提取优化信息
                if result.returncode == 0:
                    # 提取文件大小减少信息
                    for line in result.stdout.split('\n'):
                        if 'decrease' in line:
                            with self.lock:
                                print(f"Thread {thread_id} | 优化成功: {os.path.basename(file_path)}")
                                print(f"  {line.strip()}")
                else:
                    with self.lock:
                        print(f"Thread {thread_id} | 优化失败: {os.path.basename(file_path)}")
                        print(f"  错误: {result.stderr}")
                
                with self.lock:
                    self.processed_files += 1
                    progress = (self.processed_files / self.total_files) * 100
                    print(f"进度: {self.processed_files}/{self.total_files} ({progress:.1f}%)")
                    
            except queue.Empty:
                break
            except Exception as e:
                with self.lock:
                    print(f"Thread {thread_id} | 处理文件时出错: {e}")
            finally:
                self.file_queue.task_done()
    
    def run(self):
        """运行多线程优化"""
        print(f"开始查找 PNG 文件...")
        self.find_png_files()
        
        if self.total_files == 0:
            print("未找到 PNG 文件")
            return
        
        print(f"找到 {self.total_files} 个 PNG 文件")
        print(f"开始优化，使用 {self.max_threads} 个线程...")
        
        # 创建并启动线程
        threads = []
        for i in range(self.max_threads):
            thread = threading.Thread(target=self.optimize_png, args=(i+1,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # 等待所有线程完成
        self.file_queue.join()
        
        # 等待所有线程结束
        for thread in threads:
            thread.join()
        
        print(f"\n优化完成！")
        print(f"总处理文件数: {self.total_files}")
        print(f"成功处理: {self.processed_files}")

def main():
    """主函数"""
    # 配置参数
    optipng_path = os.path.join(os.path.dirname(__file__), 'pages', 'optipng.exe')
    root_dir = os.path.dirname(__file__)
    max_threads = 4  # 根据 CPU 核心数调整
    
    # 检查 optipng 是否存在
    if not os.path.exists(optipng_path):
        print(f"错误: 找不到 optipng.exe 文件")
        print(f"请确保 optipng.exe 在 {optipng_path} 位置")
        sys.exit(1)
    
    # 创建优化器并运行
    optimizer = PngOptimizer(optipng_path, root_dir, max_threads)
    optimizer.run()

if __name__ == "__main__":
    main()