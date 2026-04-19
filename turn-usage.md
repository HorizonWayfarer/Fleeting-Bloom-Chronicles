# Turn.js 翻书效果插件

## 概述

Turn.js 是一个基于 jQuery 的翻书效果插件，版本 4.1.0，用于在网页上创建逼真的 3D 翻书动画效果。该插件支持触摸屏和鼠标操作，提供流畅的翻页体验。

## 核心特性

- **3D 翻页效果**：支持两种翻页效果：`sheet`（纸张翻页）和 `hard`（硬壳书翻页）
- **双页/单页显示**：支持 `single`（单页）和 `double`（双页）两种显示模式
- **触摸支持**：自动检测触摸屏设备并使用相应的触摸事件
- **硬件加速**：支持 CSS3 硬件加速提升性能
- **渐变阴影**：可配置的翻页阴影效果增强真实感
- **页面缓存**：智能页面管理，只在 DOM 中保持必要的页面

## 快速开始

### 基本用法

```html
<div id="flipbook">
  <div class="page">第1页</div>
  <div class="page">第2页</div>
  <div class="page">第3页</div>
  <div class="page">第4页</div>
</div>

<script>
  $('#flipbook').turn({
    width: 920,
    height: 600,
    display: 'double'
  });
</script>
```

## API 参考

### Turn 方法

#### 初始化

```javascript
$('#flipbook').turn(options);
```

**默认选项**：

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `acceleration` | boolean | true | 是否启用硬件加速 |
| `display` | string | 'double' | 显示模式：'single' 或 'double' |
| `duration` | number | 600 | 翻页动画时长（毫秒） |
| `page` | number | 1 | 初始页码 |
| `gradients` | boolean | true | 是否启用渐变阴影 |
| `turnCorners` | string | 'bl,br' | 可翻页的角落 |
| `when` | object | null | 事件回调函数 |

#### 常用方法

| 方法 | 说明 | 参数 | 返回值 |
|------|------|------|--------|
| `page()` | 获取当前页码 | 无 | 当前页码 |
| `page(num)` | 跳转到指定页 | num: 页码 | jQuery 对象 |
| `next()` | 翻到下一页 | 无 | jQuery 对象 |
| `previous()` | 翻到上一页 | 无 | jQuery 对象 |
| `pages()` | 获取总页数 | 无 | 总页数 |
| `pages(num)` | 设置总页数 | num: 页数 | jQuery 对象 |
| `size()` | 获取尺寸 | 无 | {width, height} |
| `size(w, h)` | 设置尺寸 | w: 宽度, h: 高度 | jQuery 对象 |
| `display()` | 获取显示模式 | 无 | 'single' 或 'double' |
| `display(mode)` | 设置显示模式 | mode: 'single' 或 'double' | jQuery 对象 |
| `direction()` | 获取阅读方向 | 无 | 'ltr' 或 'rtl' |
| `direction(dir)` | 设置阅读方向 | dir: 'ltr' 或 'rtl' | jQuery 对象 |
| `zoom()` | 获取缩放比例 | 无 | 当前缩放值 |
| `zoom(val)` | 设置缩放比例 | val: 缩放值 (0.001-100) | jQuery 对象 |
| `disable()` | 获取禁用状态 | 无 | boolean |
| `disable(bool)` | 禁用/启用翻页 | bool: true/false | jQuery 对象 |
| `animating()` | 是否正在动画 | 无 | boolean |
| `stop()` | 停止所有动画 | 无 | jQuery 对象 |
| `peel(corner)` | 显示角落翻页效果 | corner: 角落标识 | jQuery 对象 |
| `peel(false)` | 隐藏角落效果 | 无 | jQuery 对象 |
| `addPage(el, page)` | 添加页面 | el: DOM 元素, page: 页码 | jQuery 对象 |
| `removePage(page)` | 删除页面 | page: 页码或 '*' | jQuery 对象 |
| `hasPage(page)` | 检查页面是否存在 | page: 页码 | boolean |
| `view()` | 获取当前视图 | 无 | 页码数组 |
| `view(page)` | 获取指定页的视图 | page: 页码 | 页码数组 |
| `center()` | 居中显示 | 无 | jQuery 对象 |
| `destroy()` | 销毁翻书实例 | 无 | jQuery 对象 |
| `options()` | 获取所有选项 | 无 | 选项对象 |
| `options(opts)` | 更新选项 | opts: 选项对象 | jQuery 对象 |
| `version()` | 获取版本号 | 无 | 版本字符串 |

### Flip 方法（内部使用）

| 方法 | 说明 |
|------|------|
| `flip('init', opts)` | 初始化翻页效果 |
| `flip('options', opts)` | 设置翻页选项 |
| `flip('turnPage', corner)` | 执行翻页动画 |
| `flip('peel', corner)` | 设置角落效果 |
| `flip('hide')` | 隐藏翻页效果 |
| `flip('hideFoldedPage')` | 隐藏折叠页面 |
| `flip('disable', bool)` | 禁用/启用 |
| `flip('hover', bool)` | 设置悬停效果 |

## 事件系统

### 事件列表

| 事件名 | 触发时机 | 参数 |
|--------|----------|------|
| `start` | 开始翻页时 | (options, corner) |
| `end` | 翻页结束时 | (options, turned) |
| `flip` | 完成翻页时 | 无 |
| `turning` | 正在翻页时 | (page, view) |
| `turned` | 翻页完成时 | (page, view) |
| `first` | 翻到第一页时 | 无 |
| `last` | 翻到最后一页时 | 无 |
| `pressed` | 按下页面时 | (point) |
| `released` | 释放页面时 | (point) |
| `zooming` | 正在缩放时 | (newZoom, oldZoom) |
| `zoomed` | 缩放完成时 | (page, view, oldZoom, newZoom) |
| `missing` | 检测到缺失页面时 | (pages[]) |
| `destroying` | 销毁前 | 无 |

### 事件绑定示例

```javascript
$('#flipbook').turn({
  when: {
    turned: function(event, page, view) {
      console.log('翻到第 ' + page + ' 页');
    },
    turning: function(event, page, view) {
      console.log('正在翻到第 ' + page + ' 页');
    }
  }
});

// 或使用 jQuery 事件绑定
$('#flipbook').on('turned', function(event, page, view) {
  console.log('翻到第 ' + page + ' 页');
});
```

## 角落标识

翻书效果支持以下角落标识：

| 标识 | 位置 |
|------|------|
| `tl` | 左上角 |
| `tr` | 右上角 |
| `bl` | 左下角 |
| `br` | 右下角 |
| `l` | 左侧（硬壳书模式） |
| `r` | 右侧（硬壳书模式） |

## 页面类名

页面元素会自动添加以下类名：

| 类名 | 说明 |
|------|------|
| `page` | 页面基础类 |
| `p[n]` | 页码类，如 `p1`, `p2` |
| `odd` | 奇数页 |
| `even` | 偶数页 |
| `hard` | 硬壳书效果 |
| `fixed` | 固定页面（不会被移除） |
| `own-size` | 自定义尺寸 |

## 内部数据结构

插件在 jQuery data 中存储以下数据：

```javascript
{
  opts: {},           // 选项配置
  pageObjs: {},       // 页面 DOM 对象
  pages: {},          // 翻页效果对象
  pageWrap: {},       // 页面包装器
  pageZoom: {},       // 页面缩放记录
  pagePlace: {},      // 页面位置
  pageMv: [],         // 运动中的页面
  zoom: 1,            // 当前缩放
  totalPages: 0,      // 总页数
  display: 'double',  // 显示模式
  direction: 'ltr',   // 阅读方向
  done: false,        // 是否初始化完成
  shadow: null,       // 阴影元素
  fparent: null       // 折叠页面父容器
}
```

## 辅助函数

### 数学工具

| 函数 | 说明 | 参数 |
|------|------|------|
| `rad(deg)` | 角度转弧度 | deg: 角度值 |
| `deg(rad)` | 弧度转角度 | rad: 弧度值 |
| `point2D(x, y)` | 创建二维点 | x, y: 坐标值 |
| `bezier(p1, p2, p3, p4, t)` | 贝塞尔曲线插值 | t: 0-1 |

### CSS 工具

| 函数 | 说明 |
|------|------|
| `translate(x, y, use3d)` | 创建平移变换 |
| `rotate(degrees)` | 创建旋转变换 |
| `gradient(obj, p0, p1, colors, num)` | 创建渐变效果 |
| `getPrefix()` | 获取浏览器前缀 |
| `getTransitionEnd()` | 获取过渡结束事件名 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `has(property, object)` | 检查属性是否存在 |
| `findPos(obj)` | 获取元素位置（忽略变换） |
| `hasHardPage()` | 检查是否支持硬壳书效果 |
| `rotationAvailable()` | 检查旋转功能是否可用 |

## 浏览器兼容性

- Chrome ✓
- Firefox ✓
- Safari ✓
- Opera ✓
- IE 9+ ✓（IE9 不支持硬壳书效果）

## 导出的全局变量

```javascript
$.isTouch        // 是否为触摸设备
$.mouseEvents    // 鼠标/触摸事件映射
$.cssPrefix      // 获取 CSS 前缀函数
$.cssTransitionEnd // 获取过渡结束事件函数
$.findPos        // 获取元素位置函数
```

## 示例代码

### 完整配置示例

```javascript
$('#flipbook').turn({
  width: 920,
  height: 600,
  display: 'double',
  duration: 800,
  acceleration: true,
  gradients: true,
  turnCorners: 'bl,br',
  page: 1,
  when: {
    turned: function(e, page, view) {
      console.log('当前页: ' + page);
    },
    zooming: function(e, newZoom, oldZoom) {
      console.log('缩放: ' + oldZoom + ' -> ' + newZoom);
    }
  }
});

// 动态添加页面
$('#flipbook').turn('addPage', '<div class="page">新页面</div>', 5);

// 翻到指定页
$('#flipbook').turn('page', 3);

// 缩放
$('#flipbook').turn('zoom', 0.5);
```

## 许可证

Copyright (C) 2012 Emmanuel Garcia  
All rights reserved  
查看 turnjs.com/license.txt 了解详情
