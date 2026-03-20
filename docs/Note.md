# project-management-system

a web for pms

## 功能介绍

- 项目管理
- 用户注册 支持一个邮箱多个用户！！！
- 用户密码找回
- 数据备份
  - db
  - media
  - keys
- 文档生成
- 导入导出
- 周刊

优化:

- 备份数据库的脚本需要改为celery定时任务执行.
- 迁移到生产级Web服务器

## gantt方案

gantt访问地址： http://localhost:8200/admin/projects/projectmodel/gantt/

gantt方案决策记录：

1. Google Charts Gantt（初始方案）
2. Frappe Gantt
3. DHTMLX Gantt（最终采用 ✅）

---

## Django 迁移状态不一致问题解决

### 问题描述

执行 `migrate` 报错：`django.db.utils.OperationalError: no such table: house_houseitem`

### 问题原因

数据库迁移状态与实际数据库不一致 - Django 迁移记录显示 `0001_initial` 已应用，但数据库中实际不存在表。这通常发生在数据库文件被删除或重建后。

### 解决步骤

**1. 检查迁移状态**

```bash
uv run python manage.py showmigrations house
```

结果：

```
house
 [X] 0001_initial    # Django认为已应用
 [ ] 0002_houseitem_user
```

**2. 检查迁移计划**

```bash
uv run python manage.py migrate --plan
```

**3. 将迁移标记回未应用状态（fake）**

```bash
uv run python manage.py migrate house zero --fake
```

结果：

```
Operations to perform:
  Unapply all migrations: house
Running migrations:
  Rendering model states... DONE
  Unapplying house.0001_initial... FAKED
```

**4. 重新执行迁移创建表**

```bash
uv run python manage.py migrate
```

结果：

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, house, projects, sessions, weekly
Running migrations:
  Applying house.0001_initial... OK
  Applying house.0002_houseitem_user... OK
```

**5. 验证迁移状态**

```bash
uv run python manage.py showmigrations house
```

结果：

```
house
 [X] 0001_initial
 [X] 0002_houseitem_user
```

### 关键命令说明

| 命令          | 说明                                             |
| ------------- | ------------------------------------------------ |
| `--fake`      | 只更新迁移记录，不实际修改数据库（用于同步状态） |
| `zero`        | 将应用的所有迁移回退到未应用状态                 |
| 不加 `--fake` | 实际执行 SQL 操作创建/修改表                     |
