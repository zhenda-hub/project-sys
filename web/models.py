import pdb

from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.urls import reverse

from tinymce.models import HTMLField
from markdownx.models import MarkdownxField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from mdeditor.fields import MDTextField


class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        # 说明是抽象模型类
        abstract = True

#
# class StepModel(BaseModel):
#     """步骤"""
#     name = models.CharField(verbose_name='步骤名', max_length=100)
#     status = models.BooleanField(verbose_name='项目状态', default=False)
#
#     sub_step = models.ForeignKey('self', verbose_name='子步骤', on_delete=models.CASCADE, null=True, blank=True)
#     # how = models.TextField(verbose_name='执行步骤')
#     # think = models.TextField(verbose_name='项目感想', null=True, blank=True)
#
#     def __str__(self):
#         return self.name


class ProjectModel(BaseModel):
    """项目"""
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='项目名', max_length=30)
    what = models.TextField(verbose_name='项目描述')
    why = RichTextUploadingField(verbose_name='项目意义')
    priority_choices = ((0, '低'), (1, '中'), (2, '高'))
    priority = models.IntegerField(verbose_name='优先级', default=0, choices=priority_choices)

    start_date = models.DateField(verbose_name='计划开始日期')
    end_date = models.DateField(verbose_name='计划完成日期')

    # TODO: 需要定时任务
    # is_periodic = models.BooleanField(verbose_name='是否周期性', default=False)
    # periodic_days = models.IntegerField(verbose_name='周期天数', default=1)

    # how = models.TextField(verbose_name='执行步骤')
    # how = HTMLField(verbose_name='执行步骤')
    # how = RichTextField(verbose_name='执行步骤')
    how = RichTextUploadingField(verbose_name='执行步骤', config_name='default')
    # how = MarkdownxField(verbose_name='执行步骤')
    # how = MDTextField(verbose_name='执行步骤')

    attachments = models.FileField(verbose_name='附件', upload_to='attachments/%Y/%m/%d/', null=True, blank=True)
    status = models.BooleanField(verbose_name='是否完成', default=False)
    think = models.TextField(verbose_name='项目感想', null=True, blank=True)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def duration(self):
        # pdb.set_trace()
        now_calc = (now().date() - self.start_date).days
        end_calc = (self.end_date - self.start_date).days
        if not self.status:
            return max(0, now_calc + 1)
        else:
            return min(now_calc, end_calc) + 1

    duration.fget.short_description = '已进行天数'
