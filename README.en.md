# Project Management System

A comprehensive web-based project management system built with Django's Admin, providing complete project management, user management, data backup, and more.

## ✨ Features

- **Project Management**: Create, edit, and track project progress with priority settings and status management
- **User Management**: User registration, login, password recovery, supporting multiple users per email
- **Data Backup**: Automatic backup of database, media files, and key files
- **Import/Export**: Support for data import and export functionality
- **Weekly Management**: Weekly content publishing and management
- **Permission Control**: Flexible permission management system with customizable user permissions
- **Docker Support**: Containerized deployment with CI/CD pipeline support
- **Multi-Editor Support**: CKEditor, TinyMCE, Markdown, mdeditor, vditor, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Django 4.2+
- Docker (optional)
- Docker Compose (optional)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone git@github.com:zhenda-hub/project-sys.git
   cd project-sys

   # Edit .env file to configure environment variables
   cp .env.example .env
   ```

### Docker Deployment

1. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

3. **Access the application**
   - Development: http://localhost:8200
   - Admin panel: http://localhost:8200/admin

## 📖 Examples

### Creating a New Project

1. Log in to the system and navigate to the project management module
2. Click the "New Project" button
3. Fill in project name, description, priority, and other information
4. Use the rich text editor to write detailed project execution steps
5. Set project start and end dates
6. Save the project and track progress

### User Permission Examples

- **Regular Users**: Can create and manage their own projects, view public projects
- **Administrators**: Have full access to all modules
- **System Default**: All users can log in to the admin backend, but with restricted permissions

## 🤝 Contributing

We welcome contributions of any kind! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Issue Reporting

If you encounter any issues or have improvement suggestions, please report them through:

1. Submit issues on GitHub Issues
2. Describe the detailed problem phenomenon and reproduction steps
3. Provide relevant log information or screenshots

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - Web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - API framework
- [CKEditor](https://ckeditor.com/) - Rich text editor
- [TinyMCE](https://www.tiny.cloud/) - Another excellent rich text editor
- [Docker](https://www.docker.com/) - Containerization platform
- All contributors and users for their support

---

**Note**: This project is still under active development. APIs and features may change. Please conduct thorough testing before using in production environments.
