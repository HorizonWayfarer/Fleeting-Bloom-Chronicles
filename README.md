# 刹那海棠 · Fleeting Bloom Chronicles

天津市钢管公司中学 · 高三五班电子杂志。一个**自包含**的前端电子杂志：翻页阅读同学的海棠主题文章、查看配图、听背景音乐，并支持作品点赞与留言互动。

## 技术构成

- **纯静态前端**：`index.html` 内联全部样式与逻辑，依赖 `js/lib/` 下的本地库（jQuery、turn.js 翻页、pdf.js 渲染、lightbox 看图）。**无任何外部 CDN 依赖**，字体 / 音乐 / PDF worker 均为本地文件。
- **数据**：`data/pages-map.json`（书目与配图索引）+ `docx/docs/` 下的学生文章 PDF / 图片，全部本地、自包含。
- **互动（可选）**：Cloudflare Pages Functions（`functions/api/*`）+ D1 数据库。

## 部署方式

### A. Cloudflare Pages —— 完整功能（含点赞 / 留言）

点赞与留言依赖 Cloudflare 的 **D1 数据库**，必须部署到 Cloudflare Pages 并绑定 D1 才能使用。

1. 创建 Pages 项目并连接 Git 仓库，构建输出目录设为项目根（`wrangler.toml` 中 `pages_build_output_dir = "."`）。
2. 在 Cloudflare 控制台创建 D1 数据库，名称 `fbc-comments`。
3. 项目设置 → Functions → D1 数据库绑定，变量名填 **`DB`**，选择上一步的库。
4. 首次建表：
   ```bash
   wrangler d1 execute fbc-comments --file=./schema.sql --remote
   ```
5. 推送代码触发部署。

> ⚠️ 接口使用绝对路径 `/api/*`，站点需部署在**域名根路径**（不要放在子目录）。

本地预览：`wrangler pages dev .`

### B. GitHub Pages / 任意纯静态托管 —— 无互动版

直接托管项目根目录即可，**阅读、翻页、配图、音乐全部可用**；点赞与留言因缺少 Functions / D1 不可用（前端已优雅降级，仅提示「未开启留言服务」，不影响主体阅读）。

- 可使用仓库中的 `upload-to-github.bat` 一键上传到 GitHub Pages。
- 已包含 `.nojekyll`，跳过 GitHub Pages 的 Jekyll 构建，避免路径被误处理、也更快。
- 仓库内 `docx/*.docx` 为 Word 源文件，`pages-map.json` 只引用 `docx/docs/*.pdf`；纯静态部署如需精简体积，可排除根 `docx/*.docx`。

## 目录结构（简）

```
index.html            电子杂志主页面（样式与逻辑内联）
data/                 封面、favicon、pages-map.json（书目索引）
assets/               字体、背景音乐
docx/docs/            各同学的 PDF 文章与配图（被 pages-map 引用）
js/lib/               本地前端库（jQuery / turn.js / pdf.js / lightbox / PageFlip）
functions/api/        Cloudflare Pages Functions（comments / like / essay-like）
schema.sql            D1 建表语句
*.py                  数据生成脚本（生成 pages-map、更新 media 字段、重排标记等）
upload-to-github.bat  GitHub Pages 上传工具
wrangler.toml         Cloudflare Pages + D1 配置
```

> 📌 本项目**不能用 `file://` 直接双击打开**（`index.html` 使用 ES module 与 `fetch` 加载本地 JSON，受同源策略限制）。需通过 HTTP 服务器或 `wrangler pages dev` 访问。
