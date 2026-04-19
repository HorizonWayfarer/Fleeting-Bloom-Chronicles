# 页面元素尺寸设计文档

## 📋 项目概述

本文档详细描述《岁月留痕》翻页杂志项目中所有页面元素的尺寸设计规范。

---

## 🏠 页面结构层次

```
<body>
├── #cover-page (封面页)
│   └── .cover-content (封面内容)
│       ├── h1 (标题)
│       ├── p (副标题)
│       ├── #loading (加载提示)
│       ├── .progress-container (进度条容器)
│       │   ├── .progress-bar (进度条背景)
│       │   ├── .progress-fill (进度条填充)
│       │   └── .progress-text (进度文字)
│       └── #open-book (翻开按钮)
│
├── .custom-alert-overlay (弹窗遮罩)
│   └── .custom-alert (弹窗内容)
│       ├── .custom-alert-icon (弹窗图标)
│       ├── .custom-alert-message (弹窗消息)
│       └── .custom-alert-button (弹窗按钮)
│
└── #canvas (主画布)
    ├── .zoom-icon (缩放图标)
    ├── .zoom-controls (缩放控制条)
    │   ├── .zoom-label (缩放标签)
    │   ├── #zoom-slider (缩放滑块)
    │   └── .zoom-value (缩放值显示)
    ├── .music-control (音乐控制)
    │   └── .music-icon (音乐图标)
    ├── .magazine-viewport (杂志视口)
    │   └── .container (容器)
    │       └── .magazine (杂志主体)
    │           ├── .next-button (下一页按钮)
    │           ├── .previous-button (上一页按钮)
    │           └── .page (页面)
    │               ├── .page-wrapper (页面包装器)
    │               └── .shadow (阴影)
    └── .thumbnails (缩略图区域)
        └── ul > li > img (缩略图列表)
```

---

## 📐 元素尺寸设计表

### 封面页面元素

| 元素 | 宽度 | 高度 | 定位方式 | 说明 |
|------|------|------|---------|------|
| `#cover-page` | 100% | 100% | fixed | 全屏封面，覆盖整个视口 |
| `.cover-content` | 90% (max:500px) | auto | flex子元素 | 居中的内容卡片，padding:40px |
| `h1` | auto | auto | block | 标题，字体大小3em |
| `p` | auto | auto | block | 副标题，字体大小1.2em |
| `#loading` | auto | auto | block | 加载文字提示 |
| `.progress-container` | auto | auto | block | 进度条容器，margin:20px 0 |
| `.progress-bar` | 200px | 8px | block | 进度条背景框，圆角4px |
| `.progress-fill` | 0% → 动态 | 100% | absolute | 进度条填充，带shimmer动画 |
| `.progress-text` | auto | auto | block | 百分比文字，字体0.9em |
| `#open-book` | auto | auto | inline-block | 按钮，padding:12px 30px，字体1.1em |

### 弹窗元素

| 元素 | 宽度 | 高度 | 定位方式 | 说明 |
|------|------|------|---------|------|
| `.custom-alert-overlay` | 100% | 100% | fixed | 全屏遮罩，z-index:10000 |
| `.custom-alert` | 90% (max:350px) | auto | flex居中 | 弹窗卡片，padding:30px 40px |
| `.custom-alert-icon` | auto | auto | block | 图标，字体48px |
| `.custom-alert-message` | auto | auto | block | 提示文字，字体16px |
| `.custom-alert-button` | auto | auto | inline-block | 按钮，padding:10px 30px |

### 主画布元素

| 元素 | 宽度 | 高度 | 定位方式 | 说明 |
|------|------|------|---------|------|
| `#canvas` | 100% | 100% | fixed | 主内容区域 |
| `.zoom-icon` | 22px | 22px | absolute | 缩放按钮，top:10px, right:10px |
| `.zoom-controls` | auto | auto | absolute | 缩放控制条，top:10px, 水平居中 |
| `.zoom-label` | 32px | auto | flex子元素 | 缩放标签，字体14px |
| `#zoom-slider` | 150px | 8px | inline-block | 缩放滑块，圆角4px |
| `.zoom-value` | 50px | auto | flex子元素 | 缩放值显示，字体14px |
| `.music-control` | 30px | 30px | absolute | 音乐控制按钮，top:10px, left:10px |
| `.music-icon` | 12px | 14px | inline-block | 音乐图标 |

### 杂志主体元素

| 元素 | 宽度 | 高度 | 定位方式 | 说明 |
|------|------|------|---------|------|
| `.magazine-viewport` | 100% | 100% | relative | 杂志视口容器 |
| `.container` | 922px | 600px | absolute | 杂志居中容器，top:50%, left:50% |
| `.magazine` | 922px | 600px | absolute | 杂志主体，left:-461px, top:-300px |
| `.next-button` | 22px | 600px | absolute | 右侧翻页按钮，right:-22px |
| `.previous-button` | 22px | 600px | absolute | 左侧翻页按钮，left:-22px |
| `.magazine .page` | 461px | 600px | block | 单页内容 |
| `.magazine .page-wrapper` | 100% | 100% | relative | 页面包装器 |
| `.magazine-viewport .loader` | 22px | 22px | absolute | 加载指示器 |

### 缩略图区域元素

| 元素 | 宽度 | 高度 | 定位方式 | 说明 |
|------|------|------|---------|------|
| `.thumbnails` | 100% | 140px | absolute | 缩略图区域，bottom:0 |
| `.thumbnails > div` | 90vw | 120px | block | 滚动容器，margin:20px auto |
| `.thumbnails ul` | auto | auto | block | 缩略图列表，scale:0.6 |
| `.thumbnails li` | auto | auto | inline-block | 缩略图项，margin:0 5px |
| `.thumbnails li img` | auto | auto | float | 缩略图图片 |

---

## 📱 移动端适配 (≤768px)

| 元素 | 移动端宽度 | 移动端高度 | 说明 |
|------|-----------|-----------|------|
| `#cover-page` | 95% (max:500px) | 100% | 居中显示，圆角10px |
| `.cover-content h1` | - | - | 字体2em |
| `.cover-content p` | - | - | 字体1em |
| `#open-book` | - | - | 字体1em, padding:10px 30px |
| `.thumbnails` | - | 100px | 缩短高度 |
| `.thumbnails li` | - | - | margin:0 3px |
| `.thumbnails li img` | 50px | 65px | 缩小缩略图 |
| `.zoom-controls` | - | - | 隐藏 |
| `.custom-alert` | 85% (max:300px) | auto | 缩小弹窗宽度 |
| `.custom-alert-icon` | - | - | 字体35px |
| `.custom-alert-message` | - | - | 字体15px |
| `.custom-alert-button` | - | - | 字体14px, padding:8px 25px |

---

## 🎯 尺寸设计原则

### 1. 固定尺寸策略
- **杂志主体**：922×600px 固定尺寸，保证翻页效果稳定
- **按钮控件**：固定像素尺寸，保证交互区域足够大
- **图标元素**：固定尺寸，保持视觉一致性

### 2. 百分比尺寸策略
- **全屏容器**：`#cover-page`、`#canvas` 使用100%，适应不同屏幕
- **子元素**：相对父容器使用百分比，保持布局弹性

### 3. 响应式适配策略
- **字体大小**：移动端缩小标题和按钮字体
- **容器宽度**：封面页在移动端使用95%宽度居中
- **缩略图**：缩小尺寸以适应小屏幕
- **缩放控制**：移动端隐藏滑块控制

### 4. 视口单位策略
- **缩略图容器**：使用90vw，保持两侧留白
- **最大宽度限制**：关键内容使用max-width防止过宽

### 5. 居中布局策略
- **水平居中**：使用 `margin: 0 auto` 或 flexbox
- **垂直居中**：使用flexbox布局
- **绝对居中**：杂志容器使用负margin实现居中

---

## 📊 关键尺寸关系

```
杂志总尺寸: 922px × 600px
├── 左页: 461px × 600px  (922 / 2 = 461)
└── 右页: 461px × 600px

缩略图区域: 100% × 140px
└── 滚动容器: 90vw × 120px

移动端缩略图: 50px × 65px
```

---

## 📝 修改记录

| 日期 | 修改内容 | 修改人 |
|------|---------|--------|
| 2026-04-19 | 初始版本 | 自动生成 |

---

*文档生成时间: 2026-04-19*