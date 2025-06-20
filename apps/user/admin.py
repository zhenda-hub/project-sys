from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

    
class UserAdmin(BaseUserAdmin):
    # def has_view_permission(self, request, obj=None) -> bool:
    #     super().has_view_permission(request, obj)
    #     if obj is None or request.user.is_superuser:
    #         return True
    #     return obj == request.user
    
    def get_queryset(self, request):
        """Override to filter queryset based on user permissions."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)
    
    def has_change_permission(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return True
        return obj == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return True
        return obj == request.user
    
    # inlines = [UserForWeeklyInline]
    

# Unregister the old User admin, use new UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
