from django import forms as django_forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms import fields as django_fields
from django.contrib.auth.models import User
from base import models
class BasebaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BasebaseForm, self).__init__(*args, **kwargs)


class CreateUserForm(django_forms.Form):

    username = django_fields.CharField(
        label = '账号',
        min_length = 4,
        max_length = 20,
        error_messages = { 'required':'用户名不能为空','min_length':'用户名长度不能小于4个字符','max_length':'用户名长度不能大于20个字符'}
    )

    password = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{3,32}$',
        label = '请输入密码',
        min_length = 3,
        max_length = 32,
        error_messages = {
            'requeird':'用户名不能为空',
            'invalid': '密码必须包含数字，字母、特殊字符',
            'min_length' : "密码长度不能小于3个字符",
            'max_length' : "密码长度不能大于32个字符"
        }
    )
    passwordagain = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{3,32}$',
        label='请再次输入密码',
        min_length = 3,
        max_length = 32,
        error_messages = {
            'requeird':'用户名不能为空',
            'invalid': '密码必须包含数字，字母、特殊字符',
            'min_length' : "密码长度不能小于8个字符",
            'max_length' : "密码长度不能大于32个字符"
        }
    )
    mail =django_fields.EmailField(
        label = '邮件',
    )
    name = django_fields.CharField(
        label = '用户名',
    )
    def clean(self):
        clean_data = super(CreateUserForm,self).clean()
        username = clean_data.get('username')
        if User.objects.filter(username=username):
            raise ValidationError(message='账号已存在', code='invalid')
        password = clean_data.get("password")
        passwordagain = clean_data.get("passwordagain")
        if password != passwordagain:
            raise ValidationError(message='密码需要相同', code='invalid')


class CreateServerForm(django_forms.Form):
    username = django_fields.CharField(
        label='主机名',
        min_length=4,
        max_length=20,
        widget=widgets.TextInput(attrs={'id':'username'}),
        error_messages={'required': '主机名不能为空', 'min_length': '主机名长度不能小于4个字符', 'max_length': '主机名长度不能大于20个字符'}
    )
    ext_ip = django_fields.GenericIPAddressField(
        label = '外网ip',
        widget = widgets.TextInput(attrs={'id': 'ext_ip'}),
         )
    int_ip = django_fields.GenericIPAddressField(
        label = '内网ip',
        widget=widgets.TextInput(attrs={'id': 'int_ip'}),
    )
    status = django_fields.ChoiceField(
        widget=widgets.Select(choices=[],attrs={'id': 'status'}),
        label='状态',
                                       )

    def clean(self):
        clean_data = super(CreateServerForm, self).clean()
        username = clean_data.get('username')
        ext_ip = clean_data.get('ext_ip')
        int_ip = clean_data.get('int_ip')
        if models.Base.objects.filter(hostname=username):
            raise ValidationError(message='主机名已存在', code='invalid')
        if models.Base.objects.filter(ext_ip=ext_ip):
            raise ValidationError(message='外网IP已存在', code='invalid')
        if models.Base.objects.filter(int_ip=int_ip):
            raise ValidationError(message='内网IP已存在', code='invalid')

    def __init__(self,*args,**kwargs):
        super(CreateServerForm,self).__init__(*args,**kwargs)
        d_choices = list(map(lambda x: (x[0], x[1]), models.Base.status_choices))

        self.fields['status'].choices = d_choices