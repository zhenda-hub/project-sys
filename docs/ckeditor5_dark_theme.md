# CKEditor 5 深色主题实现

## 主题切换机制

Django Admin 使用 HTML 属性 data-theme 来控制主题：

- data-theme="dark" - 手动深色模式
- data-theme="light" - 手动浅色模式
- data-theme="auto" - 跟随系统偏好

## 文件

`static/admin/css/ckeditor5-theme.css`

## 核心逻辑

### 问题

CKEditor 5 的 CSS 变量 `--ck-color-text` 定义了文本颜色，但编辑内容区域 `.ck-editor__editable` 和 `.ck-content` 没有应用该变量，导致深色模式下文字为黑色。

### 解决方案

在 CSS 变量定义后，额外添加明确的选择器规则：

```css
/* 手动深色模式 */
html[data-theme="dark"] .ck-editor__editable,
html[data-theme="dark"] .ck-content {
  color: #e0e0e0 !important;
}

/* 自动深色模式 */
@media (prefers-color-scheme: dark) {
  html[data-theme="auto"] .ck-editor__editable,
  html[data-theme="auto"] .ck-content {
    color: #e0e0e0 !important;
  }
}
```

### 关键点

- 使用 `!important` 确保优先级
- 分别处理手动模式（`data-theme="dark"`）和自动模式（`data-theme="auto"` + `@media`）
- 颜色值 `#e0e0e0` 与 `--ck-color-text` 保持一致
