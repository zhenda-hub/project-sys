from django.db import models


# 常用field备注
# user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
# public = models.BooleanField(verbose_name='是否公开', default=False)



class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        # 说明是抽象模型类
        abstract = True
