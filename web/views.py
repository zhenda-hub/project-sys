from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from .form import AdminSignupForm


def signup(request):
    if request.method == "GET":
        return render(request, "admin/signup.html", {
            'form': AdminSignupForm(),
        })
    else:
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()

            # 给用户统一分配组
            admin_group, _ = Group.objects.get_or_create(name="customer")
            user.groups.add(admin_group)

            return redirect("admin:index")
        else:
            return render(request, "admin/signup.html", {
                'form': form,
            })
