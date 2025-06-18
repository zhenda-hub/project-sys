from django.apps import AppConfig


class HouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.house'
    verbose_name = '租房管理系统'  # 这行会影响 Admin 分组显示
