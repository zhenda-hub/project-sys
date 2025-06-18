import datetime
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from apps.core.models import BaseModel


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
        db_table = 'web_weekly'
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
    """ 周刊用户, 关联到 User 模型,onetoone """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name='生日')
    life = models.PositiveSmallIntegerField(verbose_name='预期寿命', default=75)

    class Meta:
        db_table = 'web_userforweekly'
        verbose_name = '周刊用户'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return str(self.user)
