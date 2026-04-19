# Zoom.js 使用说明书

## 概述

`zoom.js` 是一个基于 jQuery 的缩放插件，专为 `turn.js` 翻页组件设计。它提供了完整的缩放功能，支持双击缩放、触摸手势、鼠标拖拽和滚轮滚动等交互方式。

## 依赖

- jQuery (1.7+)
- turn.js (翻页组件)

## 安装与引入

在引入 `zoom.js` 之前，必须先引入 jQuery 和 turn.js：

```html
<script src="jquery.min.1.7.js"></script>
<script src="turn.min.js"></script>
<script src="zoom.js"></script>
```

## 初始化配置

### 基本用法

```javascript
// 首先初始化 turn.js 翻页组件
var flipbook = $('#flipbook').turn({
  // turn.js 配置项
});

// 然后初始化 zoom 插件
$('#zoom-container').zoom({
  flipbook: flipbook  // 必填项，指定翻页组件实例
});
```

### 完整配置选项

```javascript
$('#zoom-container').zoom({
  max: 2,                    // 最大缩放级别，默认为 2
  flipbook: flipbook,        // 必填，turn.js 实例
  easeFunction: 'ease-in-out', // 过渡动画函数，默认为 'ease-in-out'
  duration: 500,             // 缩放动画持续时间（毫秒），默认为 500
  when: {                    // 事件回调函数
    zoomIn: function() {},   // 放大完成时触发
    zoomOut: function() {}   // 缩小完成时触发
  }
});
```

### 配置参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `max` | Number/Function | 否 | 2 | 最大缩放级别，可以是数值或返回数值的函数 |
| `flipbook` | Object | **是** | - | turn.js 组件实例 |
| `easeFunction` | String | 否 | 'ease-in-out' | CSS 过渡动画函数 |
| `duration` | Number | 否 | 500 | 动画持续时间（毫秒） |
| `when` | Object | 否 | {} | 事件回调配置对象 |

## API 方法

### 1. zoomIn() - 放大

```javascript
// 在指定位置放大
$('#zoom-container').zoom('zoomIn', {x: 100, y: 100});

// 在中心位置放大
$('#zoom-container').zoom('zoomIn');
```

### 2. zoomOut() - 缩小

```javascript
// 使用默认动画时长
$('#zoom-container').zoom('zoomOut');

// 指定动画时长（毫秒）
$('#zoom-container').zoom('zoomOut', 300);
```

### 3. value() - 获取当前缩放值

```javascript
var currentZoom = $('#zoom-container').zoom('value');
console.log(currentZoom); // 输出当前缩放级别
```

### 4. scroll() - 滚动视图

```javascript
// 滚动到指定位置
$('#zoom-container').zoom('scroll', {x: 50, y: 50});

// 参数说明:
// to: 目标位置 {x, y}
// unlimited: 是否允许超出边界（布尔值）
// animate: 是否使用动画（布尔值）
$('#zoom-container').zoom('scroll', {x: 50, y: 50}, false, true);
```

### 5. resize() - 重新调整缩放视图

```javascript
$('#zoom-container').zoom('resize');
```

### 6. flipbookWidth() - 获取翻书宽度

```javascript
var width = $('#zoom-container').zoom('flipbookWidth');
```

## 事件系统

### 绑定事件方式

```javascript
// 方式一：初始化时绑定
$('#zoom-container').zoom({
  flipbook: flipbook,
  when: {
    zoomIn: function() { console.log('放大完成'); },
    zoomOut: function() { console.log('缩小完成'); }
  }
});

// 方式二：使用 on() 绑定
$('#zoom-container').on('zoom.zoomIn', function() {
  console.log('放大完成');
});
```

### 可用事件列表

| 事件名称 | 触发时机 |
|----------|----------|
| `zoom.tap` | 单击页面时触发 |
| `zoom.doubleTap` | 双击页面时触发 |
| `zoom.zoomIn` | 放大操作完成时触发 |
| `zoom.zoomOut` | 缩小操作完成时触发 |
| `zoom.resize` | 缩放视图调整时触发 |
| `zoom.swipeLeft` | 向左滑动时触发（触摸设备） |
| `zoom.swipeRight` | 向右滑动时触发（触摸设备） |
| `zoom.change` | 缩放级别改变时触发（可通过 preventDefault 阻止） |

### 事件示例

```javascript
// 双击放大示例
$('#zoom-container').on('zoom.doubleTap', function(event) {
  var currentZoom = $(this).zoom('value');
  if (currentZoom > 1) {
    $(this).zoom('zoomOut');
  } else {
    $(this).zoom('zoomIn', {
      x: event.pageX,
      y: event.pageY
    });
  }
});
```

## 交互特性

### 支持的交互方式

1. **双击缩放**：在页面上双击可放大/缩小
2. **鼠标拖拽**：放大后可拖拽查看不同区域
3. **鼠标滚轮**：放大后可通过滚轮滚动
4. **触摸手势**：支持触摸设备的滑动操作

### 触摸事件支持

- `touchstart`：记录触摸起始位置
- `touchmove`：跟踪触摸移动
- `touchend`：处理滑动手势（左右滑动翻页）

## 使用示例

### 完整示例

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    #zoom-container {
      width: 800px;
      height: 600px;
      position: relative;
      overflow: hidden;
    }
    #flipbook {
      width: 100%;
      height: 100%;
    }
    .page {
      width: 400px;
      height: 600px;
      background: white;
    }
  </style>
</head>
<body>
  <div id="zoom-container">
    <div id="flipbook">
      <div class="page" page="1">第1页</div>
      <div class="page" page="2">第2页</div>
      <div class="page" page="3">第3页</div>
      <div class="page" page="4">第4页</div>
    </div>
  </div>

  <script src="jquery.min.1.7.js"></script>
  <script src="turn.min.js"></script>
  <script src="zoom.js"></script>
  <script>
    $(function() {
      // 初始化翻页组件
      var flipbook = $('#flipbook').turn({
        width: 800,
        height: 600,
        autoCenter: true
      });

      // 初始化缩放组件
      $('#zoom-container').zoom({
        flipbook: flipbook,
        max: 3,
        duration: 400,
        when: {
          zoomIn: function() {
            console.log('已放大');
          },
          zoomOut: function() {
            console.log('已缩小');
          }
        }
      });

      // 双击切换缩放
      $('#zoom-container').on('zoom.doubleTap', function(e) {
        var zoom = $(this).zoom('value');
        if (zoom > 1) {
          $(this).zoom('zoomOut');
        } else {
          $(this).zoom('zoomIn');
        }
      });
    });
  </script>
</body>
</html>
```

## 内部方法说明

### 私有方法（仅供内部使用）

| 方法 | 说明 |
|------|------|
| `_tap` | 处理单击事件 |
| `_addEvent` | 添加事件到事件队列 |
| `_eventSeq` | 判断事件序列（区分单击/双击） |
| `_prepareZoom` | 准备缩放视图 |
| `_eZoom` | 处理 turn.js 的 zooming 事件 |
| `_eStart` | 处理翻页开始事件 |
| `_eTurning` | 处理翻页中事件 |
| `_eTurned` | 处理翻页完成事件 |
| `_ePressed` | 处理按下事件 |
| `_eReleased` | 处理释放事件 |
| `_eMouseDown` | 处理鼠标按下 |
| `_eMouseMove` | 处理鼠标移动 |
| `_eMouseUp` | 处理鼠标释放 |
| `_eMouseWheel` | 处理鼠标滚轮 |
| `_eTouchStart` | 处理触摸开始 |
| `_eTouchMove` | 处理触摸移动 |
| `_eTouchEnd` | 处理触摸结束 |
| `_eDestroying` | 处理销毁事件 |

## 注意事项

1. **容器样式要求**：zoom 容器必须设置 `position: relative` 和 `overflow: hidden`
2. **flipbook 必填**：初始化时必须传入有效的 turn.js 实例
3. **触摸设备支持**：通过 `$.isTouch` 判断是否为触摸设备，自动切换事件绑定
4. **3D 变换支持**：自动检测浏览器是否支持 CSS 3D 变换（WebKitCSSMatrix 或 MozPerspective）
5. **销毁清理**：翻页组件销毁时会自动清理 zoom 相关事件和数据

## 许可证

Copyright (C) 2012 Emmanuel Garcia  
来源：www.turnjs.com  
许可证：turnjs.com/license.txt