from django import forms as django_forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms import fields as django_fields


class BasebaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BasebaseForm, self).__init__(*args, **kwargs)


class CreateUserForm(django_forms.Form):

    username = django_fields.CharField(
        label = '用户名',
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
    name = django_fields.CharField()
    def clean(self):
        clean_data = super(CreateUserForm,self).clean()
        password = clean_data.get("password")
        passwordagain = clean_data.get("passwordagain")
        if password != passwordagain:
            raise ValidationError(message='密码需要相同', code='invalid')


