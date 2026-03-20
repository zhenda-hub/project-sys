from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from tinymce.models import HTMLField
from django_ckeditor_5.fields import CKEditor5Field as RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField as CKEditor4Field
from markdownx.models import MarkdownxField
from mdeditor.fields import MDTextField

# NOTE: monkeypatching for VditorTextField
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str
from vditor.fields import VditorTextField

from apps.core.models import BaseModel


class ProjectModel(BaseModel):
    """
    项目
    :model:`auth.User`
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='项目名', max_length=30)
    what = models.TextField(verbose_name='项目描述', blank=True, null=True)
    why = RichTextUploadingField(verbose_name='项目意义', blank=True, null=True)
    priority_choices = ((0, '不重要不紧急'), (1, '不重要紧急'), (2, '重要不紧急'), (3, '重要紧急'))
    priority = models.IntegerField(verbose_name='优先级', default=0, choices=priority_choices)
    public = models.BooleanField(verbose_name='是否公开', default=False)

    start_date = models.DateField(verbose_name='计划开始日期')
    end_date = models.DateField(verbose_name='计划完成日期')

    # TODO: 需要定时任务
    # is_periodic = models.BooleanField(verbose_name='是否周期性', default=False)
    # periodic_days = models.IntegerField(verbose_name='周期天数', default=1)

    # how = models.TextField(verbose_name='执行步骤')
    # how = HTMLField(verbose_name='执行步骤')
    # how = RichTextField(verbose_name='执行步骤')

    how = RichTextUploadingField(verbose_name='执行步骤', config_name='default', blank=True, null=True)
    # how = MDTextField(verbose_name='执行步骤')

    # how = MarkdownxField(verbose_name='执行步骤')
    # how = VditorTextField(verbose_name='执行步骤')

    attachments = models.FileField(verbose_name='附件', upload_to='attachments/%Y/%m/%d/', null=True, blank=True)
    status = models.BooleanField(verbose_name='是否完成', default=False)
    think = models.TextField(verbose_name='项目感想', null=True, blank=True)
    # ck4_test = CKEditor4Field('CKEditor4测试', blank=True, null=True)  # CKEditor 4 测试字段（暂时注释）

    class Meta:
        db_table = 'web_projectmodel'
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} - {self.user}'

    @property
    def duration(self):
        """
        获得已经进行的天数
        """
        # pdb.set_trace()
        now_calc = (now().date() - self.start_date).days
        end_calc = (self.end_date - self.start_date).days
        if not self.status:
            return max(0, now_calc + 1)
        else:
            return min(now_calc, end_calc) + 1

    duration.fget.short_description = '已进行天数'
    
    
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
