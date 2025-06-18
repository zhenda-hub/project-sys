from django.apps import AppConfig


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'
    verbose_name = '项目管理'  # 这行会影响 Admin 分组显示