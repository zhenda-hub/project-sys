# 项目管理系统 (Project Management System)

一个基于Django admin 的Web项目管理系统，提供完整的项目管理、用户管理、数据备份等功能。

## ✨ 特性

- **项目管理**: 创建、编辑、跟踪项目进度，支持优先级设置和状态管理
- **用户管理**: 用户注册、登录、密码找回，支持一个邮箱多个用户
- **数据备份**: 自动备份数据库、媒体文件和密钥文件
- **导入导出**: 支持数据导入导出功能
- **周刊管理**: 周刊内容发布和管理
- **权限控制**: 灵活的权限管理系统，支持用户自定义权限
- **Docker支持**: 容器化部署，支持CI/CD流程
- **多编辑器支持**: CKEditor、TinyMCE、Markdown、mdeditor、vditor等多种编辑器

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Django 4.2+
- Docker (可选)
- Docker Compose (可选)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone git@github.com:zhenda-hub/project-sys.git
   cd project-sys
   # 编辑.env文件配置相关环境变量
   cp .env.example .env
   ```

### Docker部署

1. **使用Docker Compose启动**
   ```bash
   docker-compose up -d
   ```

2. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

3. **访问应用**
   - 开发环境: http://localhost:8200
   - 管理后台: http://localhost:8200/admin

## 📖 示例

### 创建新项目

1. 登录系统后，进入项目管理模块
2. 点击"新建项目"按钮
3. 填写项目名称、描述、优先级等信息
4. 使用富文本编辑器编写详细的项目执行步骤
5. 设置项目开始和结束日期
6. 保存项目并跟踪进度

### 用户权限示例

- **普通用户**: 可以创建和管理自己的项目，查看公开项目
- **管理员**: 拥有所有模块的完全访问权限
- **系统默认**: 所有用户都可以登录admin后台，但权限受限

## 🤝 参与贡献

我们欢迎任何形式的贡献！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 🐛 问题反馈

如果您遇到任何问题或有改进建议，请通过以下方式反馈：

1. 在GitHub Issues中提交问题
2. 描述详细的问题现象和复现步骤
3. 提供相关的日志信息或截图

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Django](https://www.djangoproject.com/) - Web框架
- [Django REST Framework](https://www.django-rest-framework.org/) - API框架
- [CKEditor](https://ckeditor.com/) - 富文本编辑器
- [TinyMCE](https://www.tiny.cloud/) - 另一个优秀的富文本编辑器
- [Docker](https://www.docker.com/) - 容器化平台
- 所有贡献者和用户的支持

---

**注意**: 本项目仍在积极开发中，API和功能可能会有变动。建议在生产环境使用前进行充分测试。
