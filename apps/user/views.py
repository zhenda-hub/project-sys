from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.conf import settings
from .form import AdminSignupForm


def signup(request):
    default_content = {
        'site_header': settings.WEB_TITLE,
        'site_title': settings.WEB_TITLE,
        'subtitle': '注册',
    }
    if request.method == "GET":
        return render(request, "admin/signup.html", {
            'form': AdminSignupForm(),
            **default_content,
        })
    else:
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True # 允许用户登录后台
            user.save()

            # 给用户统一分配组
            admin_group, _ = Group.objects.get_or_create(name="customer")
            user.groups.add(admin_group)

            return redirect("admin:index")
        else:
            return render(request, "admin/signup.html", {
                'form': form,
                **default_content,
            })
