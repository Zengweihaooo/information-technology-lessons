# 信息科技八年级上册 · 课堂资源库

[打开课程网站](https://zengweihaooo.github.io/information-technology-lessons/) · [第一单元第 4 课：智慧农场教学网页](https://zengweihaooo.github.io/information-technology-lessons/lesson.html?id=1-4)

本仓库按教材单元和课时整理课堂网页、可编辑课件、网页演示版及制作过程。

## 目录

- `docs/`：GitHub Pages 网站及供网页直接访问的最终资源。导航为 `八年级上册 → 单元 → 课时`。
- `final/`：按 `八年级上册/第一单元/第N课/` 保存的最终稿。第 1 课大体积 PPT 为避免重复存储，仅在 `docs/lessons/unit-1/lesson-1/` 保存一份。
- `drafts/`：各版 PPT、网页、视频草稿和构建源码。
- `课程目录.md`：四个单元的课程纲目。

PPT 的网页演示由 PDF 页面渲染为图片，支持上/下页、方向键和全屏。可编辑 PPT 原件保留在仓库。体积超过 GitHub 单文件常规限制的资料使用 Git LFS，下载前请安装 Git LFS 并执行 `git lfs pull`。

## 新增课时

1. 在 `final/八年级上册/第X单元/第Y课/` 放入最终稿，过程版本放入对应的 `drafts/` 目录。
2. 需要网页访问的文件放到 `docs/lessons/unit-X/lesson-Y/`。
3. 在 `docs/assets/site.js` 的 `units`、`available`、`res` 中登记课时与资源。
4. PPT 可转为 PDF，再逐页渲染到 `docs/assets/slides/lesson-Y/slide-01.jpg` 等，并设置总页数。

## 原始资料说明

教材 PDF 是第三方出版物，未放入公开仓库。课代表表格涉及学生资料收集，也未上传。自动生成的缓存、依赖目录和重复渲染中间文件未归档；保留了可编辑稿、主要过程稿和构建源码。
