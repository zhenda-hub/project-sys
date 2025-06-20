from django.contrib import admin
from django.db.models import Q

# Register your models here.


# 个性化设置
admin.site.site_title = '管理系统平台'
admin.site.site_header = '管理系统平台'
admin.site.index_title = '管理平台首页'
admin.site.site_url = None  # 没有site


class DefaultMixin():
    """
    默认的admin mixin
    
    1. 如果是超级用户，则可以查看所有
    2. 否则只能查看自己的
    """
    def save_model(self, request, obj, form, change):
        obj.user = request.user  # 设置当前用户为创建者
        # pdb.set_trace()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """list view"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        """change view"""
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        """delete view"""
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class PublicMixin(DefaultMixin):
    """有 public的admin mixin"""

    def get_queryset(self, request):
        """list view"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(user=request.user) | Q(public=True))
