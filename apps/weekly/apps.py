from django.apps import AppConfig


class WeeklyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.weekly'
    verbose_name = '人生倒计时系统'  # 这行会影响 Admin 分组显示