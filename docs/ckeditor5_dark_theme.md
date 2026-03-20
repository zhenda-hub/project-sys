# CKEditor 5 深色主题实现

## 主题切换机制

Django Admin 使用 HTML 属性 data-theme 来控制主题：

- data-theme="dark" - 手动深色模式
- data-theme="light" - 手动浅色模式
- data-theme="auto" - 跟随系统偏好

## 文件

`static/admin/css/ckeditor5-theme.css`

---

## 问题 1: 深色模式下编辑器文字为黑色

### 根因

CKEditor 5 的 CSS 变量 `--ck-color-text` 定义了文本颜色，但编辑内容区域 `.ck-editor__editable` 和 `.ck-content` 没有应用该变量。

### 解决方案

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

---

## 问题 2: h2/h3/h4 标题有多余的 padding

### 根因

Django Admin 的 `static/admin/css/base.css` 中有如下样式：

```css
/* base.css:567 */
.module p, .module ul, .module h3, .module h4, .module dl, .module pre {
    padding-left: 10px;
    padding-right: 10px;
}

/* base.css:584 */
.module h2, .module caption, .inline-group h2 {
    padding: 8px;
    /* ... */
}
```

当 CKEditor 5 编辑器位于 `.module` 容器内时，其内容区域的 h2/h3/h4 标题继承了这些 padding 样式。

### 解决方案

**注意：此问题与 theme 无关，只需写一次通用规则**

```css
/* 修复 base.css 导致的标题 padding 问题 */
.module .ck-content h2,
.module .ck-content h3,
.module .ck-content h4 {
    padding: 0 !important;
    margin-top: 0 !important;
}
```

### 调试方法

使用浏览器开发者工具（F12）检查 h2/h3/h4 元素的 Computed 样式，找到 padding 的来源。

---

## 完整配置示例

```css
/* CKEditor 5 跟随 Django Admin 主题 */

/* 当 Admin 是 dark 主题时 */
html[data-theme="dark"] .ck-editor {
    --ck-color-base-background: #1e1e1e;
    --ck-color-base-border: #3a3a3a;
    --ck-color-text: #e0e0e0;
    /* ... 其他颜色变量 */
}

/* 修复文字颜色 */
html[data-theme="dark"] .ck-editor__editable,
html[data-theme="dark"] .ck-content {
    color: #e0e0e0 !important;
}

/* 修复标题 padding */
html[data-theme="dark"] .module .ck-content h2,
html[data-theme="dark"] .module .ck-content h3,
html[data-theme="dark"] .module .ck-content h4 {
    padding: 0 !important;
    margin-top: 0 !important;
}

/* Auto 模式同理 */
@media (prefers-color-scheme: dark) {
    /* ... */
}
```
