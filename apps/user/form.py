from enum import unique
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError


class AdminSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if (
    #         email
    #         and self._meta.model.objects.filter(email=email).exists()
    #     ):
    #         self._update_errors(
    #             ValidationError(
    #                 {
    #                     "email": self.instance.unique_error_message(
    #                         self._meta.model, ["email"]
    #                     )
    #                 }
    #             )
    #         )
    #     else:
    #         return email
        
    class Meta:
        model = User
        fields = ["username", "email"]  # 字段与模型定义完全一致且不需要额外定制, password通过继承手动定制处理。
        """
        get_or_create()
        update_or_create()
        get_object_or_404()
        
        """
