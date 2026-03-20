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

---

## 附录：CKEditor 4 vs CKEditor 5 架构对比

### 渲染方式差异

| 特性 | CKEditor 4 | CKEditor 5 |
|------|------------|------------|
| 渲染方式 | **iframe** | **div** (contentEditable) |
| 样式隔离 | ✅ 自动隔离 | ❌ 共享页面 CSS |
| 主题切换 | ❌ 需销毁重建编辑器 | ✅ CSS 变量实时生效 |
| 维护状态 | ⚠️ 停止维护（有安全警告） | ✅ 活跃维护 |

### 为什么 CKEditor 5 不用 iframe

CKEditor 5 放弃 iframe，采用 **虚拟 DOM + contentEditable** 架构：

1. **自建虚拟 DOM 引擎** - MVC 架构（Model → View → DOM）
2. **解决 contentEditable 浏览器差异** - 用虚拟层抽象
3. **更轻量、更灵活、扩展性更强**

**代价：** 需要手动处理外部 CSS 干扰（如本文档解决的问题）

### CKEditor 4 不适合动态主题切换

CKEditor 4 虽然支持 Moono Dark 暗色皮肤，但**无法运行时动态切换**：

> "The only way to change skin is from the config... you need to **destroy and recreate** the editor"

动态切换会导致：
- ❌ 编辑器内容可能丢失
- ❌ 光标位置丢失
- ❌ 用户体验差

因此，**需要跟随 Django Admin 主题动态切换的场景，推荐使用 CKEditor 5**。

### 参考

- [Introduction to CKEditor 5 architecture](https://ckeditor.com/docs/ckeditor5/latest/framework/architecture/intro.html)
- [Editing engine | CKEditor 5 Framework Documentation](https://ckeditor.com/docs/ckeditor5/latest/framework/architecture/editing-engine.html)
- [Dynamic update of CKEditor skin - Stack Overflow](https://stackoverflow.com/questions/33799993/dynamic-update-of-ckeditor-skin)
- [Moono Dark Skin - CKEditor Add-ons](https://ckeditor.com/cke4/addon/moono-dark)
