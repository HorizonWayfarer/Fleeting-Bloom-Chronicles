# 岁月留痕 (Fleeting Bloom Chronicles)

## 项目介绍

《岁月留痕》是一个基于 Turn.js 和 PDF.js 开发的翻页杂志项目，以"海棠花"为主题，记录高三五班学生的青春回忆与校园故事。项目采用复古文艺风格，融合米色与棕色的温暖色调，营造怀旧氛围。

## 快速访问

- **在线示例**：[https://fleeting-bloom-chronicles.pages.dev/](https://fleeting-bloom-chronicles.pages.dev/) | [https://baymelody.ccwu.cc/](https://baymelody.ccwu.cc/)
- **GitHub 仓库**：[https://github.com/HorizonWayfarer/Fleeting-Bloom-Chronicles](https://github.com/HorizonWayfarer/Fleeting-Bloom-Chronicles)

## 功能特性

- **精美的翻页动画**：使用 Turn.js 实现流畅的翻页效果，模拟真实书籍的翻页体验
- **PDF驱动内容**：使用 PDF.js 从 PDF 文件动态渲染页面，支持单页/双页显示
- **封面页面交互**：打开网页首先看到封面，点击"翻开"按钮后进入杂志内容
- **加载进度条**：实时显示字体加载、PDF下载和缩略图生成进度，带动态光效
- **背景音乐**：集成背景音乐，增强阅读体验，点击图标控制播放/暂停
- **缩略图导航**：支持横向滚动的缩略图导航，可快速定位到任意页面
- **悬停放大效果**：鼠标悬停在缩略图上时会从鼠标位置放大，提升用户体验
- **平滑滚动**：点击缩略图后会平滑滚动到选中的页面
- **响应式设计**：适配不同屏幕尺寸，移动端自动切换单页显示模式
- **自定义弹窗**：美观的加载提示弹窗，与整体风格保持一致
- **缩放控制**：支持页面放大缩小，配有滑块控制器精确调节缩放比例
- **键盘快捷键**：支持左右方向键翻页，ESC键退出缩放模式
- **触摸支持**：支持触摸设备的滑动翻页和双指缩放操作

## 技术实现

- **前端框架**：HTML5, CSS3, JavaScript
- **核心库**：Turn.js (翻页效果), PDF.js (PDF渲染), jQuery (DOM操作)
- **音频处理**：HTML5 Audio API
- **动画效果**：CSS3 Transitions, Transformations, Keyframes
- **响应式设计**：Media Queries
- **缩放功能**：zoom.js
- **触摸手势**：jGestures
- **URL路由**：hash.js

## 目录结构

```
Fleeting-Bloom-Chronicles/
├── css/                 # 样式文件
│   ├── jquery.ui.css
│   ├── jquery.ui.html4.css
│   └── magazine.css     # 主样式文件
├── extras/              # 额外资源
│   ├── Wild - All My Life_min.mp3    # 背景音乐
│   ├── LXGWWenKaiLite-Medium.ttf     # 霞鹜文楷字体(TTF)
│   ├── LXGWWenKaiLite-Medium.woff2   # 霞鹜文楷字体(WOFF2)
│   ├── Dutch 801 Roman BT.ttf        # Dutch 801 Roman字体
│   ├── jquery.min.1.7.js
│   ├── jquery-ui-1.8.20.custom.min.js
│   ├── jquery.mousewheel.min.js
│   ├── modernizr.2.5.3.min.js
│   └── jgestures.min.js              # 触摸手势库
├── js/                  # 自定义脚本
│   ├── magazine.js      # 杂志核心功能
│   ├── pdf.min.js       # PDF.js核心库
│   └── pdf.worker.min.js # PDF.js Web Worker
├── lib/                 # 核心库
│   ├── turn.js          # 翻页效果库
│   ├── turn.min.js      # 翻页效果库(压缩版)
│   ├── turn.html4.js    # IE8兼容版本
│   ├── turn.html4.min.js
│   ├── zoom.js          # 缩放功能
│   ├── zoom.min.js      # 缩放功能(压缩版)
│   ├── hash.js          # URL哈希处理
│   ├── scissor.js       # 裁剪功能
│   └── scissor.min.js   # 裁剪功能(压缩版)
├── pages/               # 杂志内容
│   ├── magazine.pdf     # PDF杂志文件(主文件)
│   ├── magazine1.pdf    # PDF杂志文件(备用)
│   ├── magazine3.pdf    # PDF杂志文件(备用)
│   ├── optipng.exe      # PNG优化工具
│   └── 递归转渐进图_修复版.bat  # 图片处理脚本
├── pics/                # 界面图片
│   ├── arrows.png       # 翻页箭头图标
│   ├── loader.gif       # 加载动画
│   ├── zoom-icons.png   # 缩放图标
│   ├── zoom-icons-editable.png # 缩放图标(可编辑)
│   └── zoom.png         # 缩放相关图片
├── index.html           # 主页面
├── index - 副本.html    # 页面副本
├── favicon.ico          # 网站图标
├── share_server.py      # 简易共享服务器
├── generate_magazine.py # 杂志生成脚本
├── optimize_pngs.py     # PNG优化脚本
├── images.txt           # 图片列表
├── output.txt           # 输出日志
├── update.txt           # 更新记录
├── turn-usage.md        # Turn.js使用说明
├── zoom-usage.md        # Zoom.js使用说明
├── ELEMENTS_DIMENSIONS.md # 元素尺寸设计文档
└── README.md            # 项目说明
```

## 安装与使用

### 1. 克隆或下载项目

### 2. 启动本地服务器

由于浏览器的安全限制，直接打开 HTML 文件可能会导致某些功能无法正常工作。建议使用本地服务器运行项目：

#### 使用 Python 启动服务器

```bash
# 在项目根目录执行
python -m http.server 8000
```

#### 使用 Node.js 启动服务器

```bash
# 安装 http-server（如果未安装）
npm install -g http-server

# 在项目根目录执行
http-server -p 8000
```

#### 使用项目自带脚本

```bash
# 使用 Python 脚本启动共享服务器
python share_server.py
```

### 3. 访问项目

在浏览器中打开 `http://localhost:8000/index.html` 即可访问项目。

## 使用说明

1. **打开页面**：首先看到封面，等待加载完成后点击"翻开"按钮进入杂志内容
2. **翻页**：
   - 鼠标点击页面边缘或使用左右箭头按钮翻页
   - 触摸设备上可滑动翻页
   - 使用键盘左右方向键翻页
3. **导航**：
   - 使用底部的缩略图导航栏快速定位页面
   - 鼠标滚轮可横向滚动缩略图
   - 触摸设备可滑动缩略图区域
   - 点击缩略图直接跳转到对应页面
4. **音乐控制**：
   - 点击左上角的音乐图标控制音乐播放/暂停
5. **缩放**：
   - 点击右上角的放大图标进入缩放模式
   - 使用滑块精确调节缩放比例
   - 点击缩小图标或按 ESC 键退出缩放模式
   - 缩放模式下支持手势操作

## 自定义与扩展

### 添加新内容

1. 替换 `pages/magazine.pdf` 文件即可更新杂志内容
2. PDF文件会自动渲染，无需修改代码

### 修改背景音乐

1. 将新的音乐文件替换 `extras/Wild - All My Life_min.mp3`
2. 确保音乐文件格式为 MP3

### 调整样式

修改 `css/magazine.css` 文件可以调整项目的视觉样式，包括颜色、字体、布局等。

### 修改字体

项目使用两种字体：
- **Dutch 801 Roman**：默认字体，用于标题和主要文字
- **LXGW WenKai**：备用字体，用于中文显示

可在 `index.html` 的 `<style>` 块中修改字体配置。

### 图片优化

使用 `optimize_pngs.py` 脚本可以批量优化项目中的 PNG 图片：

```bash
python optimize_pngs.py
```

## 浏览器兼容性

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 注意事项

1. **性能优化**：PDF文件会缓存到内存中，翻页时直接使用
2. **文件路径**：确保所有文件路径正确，特别是PDF和字体文件
3. **浏览器安全限制**：在本地直接打开 HTML 文件可能会导致音频无法自动播放，建议使用本地服务器
4. **响应式设计**：在不同屏幕尺寸上会自动调整布局，移动端显示单页
5. **缩放模式**：在缩放模式下，翻页按钮会隐藏，使用键盘或手势操作

## 项目英文名

**Fleeting Bloom Chronicles**

- **Fleeting** - 短暂的、转瞬即逝的
- **Bloom** - 绽放
- **Chronicles** - 编年史

寓意青春如海棠花般短暂而绚烂，值得被永久珍藏。

---

*文档生成时间: 2026-04-19*