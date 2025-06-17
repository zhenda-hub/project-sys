import pdb
import datetime

from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.urls import reverse

from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from markdownx.models import MarkdownxField
from mdeditor.fields import MDTextField

# NOTE: monkeypatching for VditorTextField
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str
from vditor.fields import VditorTextField


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
    """
    项目
    :model:`auth.User`
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='项目名', max_length=30)
    what = models.TextField(verbose_name='项目描述')
    why = RichTextUploadingField(verbose_name='项目意义')
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

    how = RichTextUploadingField(verbose_name='执行步骤', config_name='default')
    # how = MDTextField(verbose_name='执行步骤')

    # how = MarkdownxField(verbose_name='执行步骤')
    # how = VditorTextField(verbose_name='执行步骤')

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


class Weekly(BaseModel):
    """
    周刊
    :model:`auth.User`
    """
    date = models.DateField(verbose_name='创建日期', default=datetime.date.today)  # 默认值不能调用，...
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    public = models.BooleanField(verbose_name='是否公开', default=False)

    content = RichTextUploadingField(verbose_name='周刊内容', config_name='default')
    # content = MDTextField(verbose_name='周刊内容')

    attachments = models.FileField(verbose_name='附件', upload_to='attachments/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = '周刊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user} {self.date}'
    
    @property
    def time_left(self):
        try:
            birthday = self.user.userforweekly.birthday
            life = self.user.userforweekly.life
        except:
            return ''
        memorial_day = birthday + datetime.timedelta(days=365) * life
        total_days = (memorial_day - self.date).days
        return f'星期: {total_days // 7}, 月: {total_days // 30}, 年: {total_days // 365}'

    time_left.fget.short_description = '剩余时间'


class UserForWeekly(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name='生日')
    life = models.PositiveSmallIntegerField(verbose_name='预期寿命', default=75)

    class Meta:
        verbose_name = '周刊用户'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return str(self.user)



class House(BaseModel):
    """房屋模型"""
    name = models.CharField(max_length=100, verbose_name="房屋名称")
    address = models.TextField(verbose_name="地址")
    area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="面积(m²)", null=True, blank=True)
    
    status_choices = [
        ('available', '可租'),
        ('rented', '已租'),
        ('maintenance', '维修中')
    ]
    status = models.CharField(max_length=20, choices=status_choices,default='available', verbose_name="状态")
    monthly_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="月支出")
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="月租金", null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    class Meta:
        verbose_name = "房屋"
        verbose_name_plural = "房屋管理"
        
    @property
    def monthly_income(self):
        """计算月净收入"""
        return self.monthly_rent - self.monthly_expense

class HouseItem(BaseModel):
    """房屋物品模型"""
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='items', verbose_name="所属房屋")
    name = models.CharField(max_length=100, verbose_name="物品名称")
    price = models.DecimalField('单价', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    
    condition_choices = [
        ('good', '良好'),
        ('damaged', '损坏'),
        ('lost', '丢失')
    ]
    condition = models.CharField(max_length=20, choices=condition_choices, default='good', verbose_name="状态")
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return f"{self.name} ({self.get_condition_display()})"

    class Meta:
        verbose_name = "物品"
        verbose_name_plural = "物品管理"
        
    @property
    def total_price(self):
        return self.price * self.quantity
