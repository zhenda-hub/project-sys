from django.db import models
from apps.core.models import BaseModel



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
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="月租金", default=0.00)
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    class Meta:
        db_table = 'web_house'
        verbose_name = "房屋"
        verbose_name_plural = verbose_name
        
    @property
    def monthly_income(self):
        """计算月净收入"""
        return self.monthly_rent - self.monthly_expense
    
    monthly_income.fget.short_description = '月净收入'


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
        db_table = 'web_houseitem'
        verbose_name = "物品"
        verbose_name_plural = verbose_name
        
    @property
    def total_price(self):
        return self.price * self.quantity

    total_price.fget.short_description = '总价'
