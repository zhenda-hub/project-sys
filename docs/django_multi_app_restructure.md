# Django项目多App重构计划

## 目标
将当前单app(web)结构重构为多app结构，按功能模块划分

## 新目录结构
```
project_sys/
├── apps/                  # 存放所有Django应用的目录
│   ├── core/              # 核心功能app (原web中的基础功能)
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # 基础模型(如User等)
│   │   └── views.py
│   ├── projects/          # 项目管理相关功能
│   ├── weekly/            # 周报相关功能
│   └── house/             # 房屋管理相关功能
├── project_sys/           # 项目配置目录
├── utils/                 # 工具类
├── templates/             # 全局模板
└── static/                # 全局静态文件
```

## 重构步骤
1. **分析现有模型**
   - 检查web/models.py，按功能拆分模型
   - 识别共享模型(如User等)放入core app

2. **创建新app结构**
   ```bash
   python manage.py startapp core apps/core
   python manage.py startapp projects apps/projects
   python manage.py startapp weekly apps/weekly
   python manage.py startapp house apps/house
   ```

3. **迁移模型和代码**
   - 将相关模型移动到对应app
   - 迁移关联的views、forms等代码
   - 处理外键关系变更

4. **更新配置**
   - 修改settings.py中的INSTALLED_APPS
   - 配置新app的静态文件和模板路径

5. **URL路由调整**
   - 为每个app创建urls.py
   - 更新项目根urls.py包含各app路由

## 注意事项
- 数据库迁移可能需要特殊处理
- 确保所有模型导入路径更新
- 测试所有功能迁移后的可用性
