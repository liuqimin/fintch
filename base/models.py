from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import  User
# Create your models here.
class Base(models.Model):
    status_choices = (
        (1,'使用'),
        (2,'未使用'),
        (3,'下线'),
    )
    hostname = models.CharField('服务器名',max_length=32)
    ext_ip = models.GenericIPAddressField()
    int_ip = models.GenericIPAddressField()
    status = models.IntegerField(choices = status_choices)
    class Meta:
        verbose_name = '基础表'
        verbose_name_plural = '基础表'
    def __str__(self):
        return self.hostname

class Service(models.Model):
    status_choices = (
        ('uat', '测试环境'),
        ('prd', '生产环节'),
        ('demo', '演示环境'),
    )
    jar_choices = (
        (1,'是'),
        (2,'否'),
    )
    servidor = models.ForeignKey('Base')
    app = models.CharField('服务名',max_length=32)
    entorno = models.CharField('环境',max_length=8,choices=status_choices)
    port = models.IntegerField('端口')
    is_jar_or_war = models.CharField('是否jar或者war',max_length=2,choices=jar_choices)
    jar = models.CharField('java包名',max_length=32,null=True,blank=True)
    #jar_load = models.CharField('java路径',max_length=32,null=True,blank=True)
    start_user = models.CharField('启动用户',max_length=8)
    #start_script = models.FilePathField('启动命令',max_lenth)
    class Meta:
        verbose_name = '服务表'
        verbose_name_plural = '服务表'

    def __str__(self):
        returninfo = '{}-{}'.format(self.app,self.port)
        return returninfo

class Project(models.Model):
    servidor = models.ManyToManyField('Base')
    proyecto = models.CharField('项目名',max_length=32)

    class Meta:
        verbose_name = '项目表'
        verbose_name_plural = '项目表'
    def __str__(self):
        return self.proyecto

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name