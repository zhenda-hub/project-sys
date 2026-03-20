# MDEditor 图片上传配置指南

## 问题描述

MDEditor 上传图片后，编辑器显示 `![]()` 而不是 `![](/media/editor/xxx.png)`，图片无法正确插入。

## 错误信息

```
Refused to display 'http://localhost:8002/' in a frame because it set 'X-Frame-Options' to 'deny'.
Uncaught SecurityError: Failed to read a named property 'document' from 'Window': Blocked a frame with origin "http://localhost:8002" from accessing a cross-origin frame.
```

## 根因分析

### 原因 1: X-Frame-Options 阻止 iframe 访问

Django 默认设置 `X-Frame-Options: DENY`，阻止页面被 iframe 嵌入。MDEditor 的图片上传对话框使用 iframe，导致跨域错误。

### 原因 2: MEDIA_URL 缺少前导斜杠

```python
MEDIA_URL = 'media/'  # ❌ 错误
```

### 原因 3: 缺少 MDEditor URL 配置

`urls.py` 中缺少 MDEditor 的 URL 路由，导致上传接口 404。

---

## 解决方案

### 1. 修改 settings.py

#### 1.1 修正 MEDIA_URL

```python
# 修改前
MEDIA_URL = 'media/'

# 修改后
MEDIA_URL = '/media/'
```

#### 1.2 添加 X-Frame-Options

```python
# 允许同源 iframe（MDEditor 图片上传需要）
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

#### 1.3 确认 MDEDITOR_CONFIGS 配置

```python
MDEDITOR_CONFIGS = {
    'default': {
        # ... 其他配置
        'upload_image_url': '/mdeditor/uploads/',  # ✅ 必须配置
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        'image_folder': 'editor',  # 图片保存到 media/editor/
    }
}
```

### 2. 修改 urls.py

```python
urlpatterns = [
    # ...
    path('mdeditor/', include('mdeditor.urls')),  # ✅ 必须添加
]
```

---

## 验证步骤

1. **重启 Django 服务器**
2. **打开 Django Admin** → 编辑带 MDEditor 字段的模型
3. **点击图片上传按钮** → 选择图片 → 上传
4. **检查编辑器**：应该显示 `![](/media/editor/xxx.png)`
5. **切换到预览模式**：图片应正确显示

---

## 文件

- `project_sys/settings.py` - MEDIA_URL, X_FRAME_OPTIONS, MDEDITOR_CONFIGS
- `project_sys/urls.py` - mdeditor URLs

---

## 附录：MDEditor vs CKEditor 5 功能对比

| 特性 | MDEditor | CKEditor 5 |
|------|----------|------------|
| 图片上传 | ✅ | ✅ |
| 动态主题切换 | ❌ 不支持 | ✅ CSS 变量实时切换 |
| 跟随系统主题 | ❌ 不支持 | ✅ 支持 |
| Markdown 编辑 | ✅ | ❌ |
| 所见即所得 | ❌ 需预览 | ✅ |
| X-Frame-Options | ⚠️ 需要 SAMEORIGIN | ✅ 无特殊要求 |

**建议**：
- 如果需要 Markdown 编辑 → 使用 MDEditor
- 如果需要动态主题切换 → 使用 CKEditor 5
