from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class Asset(models.Model):
    '''
    固定资产
    '''
    type_choices = (
        (1, '笔记本'),
        (2, '台式机'),
        (3, '显示器'),

    )
    status_choices = (
        (1, '使用'),
        (2, '未使用'),
    )
    ni = models.BigAutoField(primary_key=True)
    sn = models.CharField('SN号',max_length=32,unique=True)
    asset_model = models.ForeignKey(verbose_name='型号',to='asset_model',max_length=32,null=True)
    type = models.IntegerField(verbose_name='类型',choices = type_choices)
    user = models.ForeignKey(verbose_name='使用人',to='Member',to_field='nid',null=True)
    status = models.IntegerField(verbose_name='状态',choices=status_choices)
    macaddress = models.CharField(verbose_name='MAC地址',max_length=128,unique=True,null=True,blank=True)
    ipaddress = models.GenericIPAddressField(verbose_name='IP地址',null=True,blank=True)

   # status = models.IntegerField(choices = status_choices)
    class Meta:
        verbose_name = '固定资产'
        verbose_name_plural = '固定资产'
    def __str__(self):
        return self.sn

class asset_model(models.Model):
    '''
    固定资产型号
    '''
    nid = models.BigAutoField(primary_key=True)
    name = models.CharField('型号',max_length=32)
    def __str__(self):
        return self.name
class Member(models.Model):
    """
    用户表
    """
    computer_choices = (
        (1, '博莹'),
        (2, '信产所'),

    )
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='姓名', max_length=32, unique=True)
    computer = models.IntegerField('类型', choices=computer_choices)
    def __str__(self):
        return self.username