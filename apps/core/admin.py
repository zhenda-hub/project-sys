from django.contrib import admin
from django.db.models import Q

# Register your models here.


# 个性化设置
admin.site.site_title = '管理系统平台'
admin.site.site_header = '管理系统平台'
admin.site.index_title = '管理平台首页'
admin.site.site_url = None  # 没有site


class MyMixin():
    def save_model(self, request, obj, form, change):
        obj.user = request.user  # 默认设置当前用户为评论者
        # pdb.set_trace()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # 用户只能查看自己的和公开的
        qs = super().get_queryset(request)
        return qs.filter(Q(user=request.user) | Q(public=True))

    def has_change_permission(self, request, obj=None):
        # 用户只能修改自己的，不能修改别人的
        if obj is None:
            return True

        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        # 用户只能删除自己的，不能删除别人的
        if obj is None:
            return True

        return obj.user == request.user
    
    