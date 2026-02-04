# project-management-system

a web for pms

## 功能介绍

-   项目管理
-   用户注册 支持一个邮箱多个用户！！！
-   用户密码找回
-   数据备份
    -   db
    -   media
    -   keys
-   文档生成
-   导入导出
-   周刊

优化:

- 改为使用 docker compose 和  cicd 优化开发和部署.
- 备份数据库的脚本需要改为celery定时任务执行.


容器化应用
设置基本CI/CD流程
迁移到生产级Web服务器


房屋  地址、价格、面积、图片、描述等
物品 订单 账单

 Vue 3 + Element Plus + Supabase 的组合

用户方案: one2one

TODO:
日志记录:


我计划把admin当管理系统来使用, 需要对django默认用户扩展, 采用 one2one 来扩展属性后, 需要控制权限, 具体权限需求如下:

1. 所有用户可以登录admin
2. 所有用户默认,
   - 其他模块:
     - 自己创建内容的所有权限
     - 查看公开内容的权限
3. 真正管理员 控制所有的权限




gantt访问地址： http://localhost:8200/admin/projects/projectmodel/gantt/

gantt方案决策记录：
  1. Google Charts Gantt（初始方案）
  2. Frappe Gantt
  3. DHTMLX Gantt（最终采用 ✅）

---

## ImportExportModelAdmin 模板覆盖难点

### 问题描述
在 `ImportExportModelAdmin` 的项目列表页面添加自定义按钮（如"甘特图"）时，使用常规的 `admin/change_list.html` 模板覆盖方法无效。

### 原因分析
`ImportExportModelAdmin` 使用的是 `admin/import_export/change_list_import_export.html` 模板，而不是 Django 默认的 `admin/change_list.html`。

当你创建 `templates/admin/projects/change_list.html` 时，Django 不会使用它，因为 `ImportExportModelAdmin` 已经指定了自己的模板。

### 解决方案

#### 方法 1：在 admin.py 中指定自定义模板（推荐）

**步骤：**

1. 在 `ProjectModelAdmin` 类中指定自定义模板：
```python
class ProjectModelAdmin(DefaultMixin, ImportExportModelAdmin):
    import_export_change_list_template = "admin/projects/change_list_import_export.html"
```

2. 创建模板文件 `apps/projects/templates/admin/projects/change_list_import_export.html`：
```django
{% extends "admin/import_export/change_list_import_export.html" %}
{% load i18n %}

{% block object-tools-items %}
  {{ block.super }}
  <li>
    <a href="/admin/projects/projectmodel/gantt/" class="button">甘特图</a>
  </li>
{% endblock %}
```

**关键点：**
- 继承 `admin/import_export/change_list_import_export.html` 而不是 `admin/change_list.html`
- 只调用 `{{ block.super }}` 来获取父模板的导入/导出按钮
- 不要重复 `{% include "admin/import_export/change_list_import_item.html" %}`，否则按钮会重复显示

#### 方法 2：覆盖全局 import_export 模板（不推荐）
在 `templates/admin/import_export/change_list_import_export.html` 中添加按钮，但这会影响所有使用 ImportExportModelAdmin 的应用。

### 相关文件
- `apps/projects/admin.py` - 添加 `import_export_change_list_template` 配置
- `apps/projects/templates/admin/projects/change_list_import_export.html` - 自定义模板

---

## 数据导出HTML标签问题

### 问题描述
使用 `RichTextUploadingField` 的字段导出到 Excel 时，包含 HTML 标签，用户只需要纯文本。

### 影响范围
- `ProjectModelResource` in `apps/projects/admin.py` - 字段: `why`, `how`
- `WeeklyResource` in `apps/weekly/admin.py` - 字段: `content`

### 解决方案
在 Resource 类中重写 `dehydrate_<fieldname>()` 方法，使用 Django 内置的 `strip_tags` 工具去除 HTML 标签。

### 修改文件

#### 1. `apps/projects/admin.py`
```python
from django.utils.html import strip_tags

class ProjectModelResource(resources.ModelResource):
    class Meta:
        model = ProjectModel

    def dehydrate_why(self, obj):
        return strip_tags(obj.why)

    def dehydrate_how(self, obj):
        return strip_tags(obj.how)
```

#### 2. `apps/weekly/admin.py`
```python
from django.utils.html import strip_tags

class WeeklyResource(resources.ModelResource):
    class Meta:
        model = Weekly

    def dehydrate_content(self, obj):
        return strip_tags(obj.content)
```
