from django import forms as django_forms
from django.forms import widgets
from django.forms import fields as django_fields


class BasebaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BasebaseForm, self).__init__(*args, **kwargs)


class CreateUserForm(BasebaseForm,django_forms.Form):
    username = django_fields.CharField(
        min_length = 4,
        max_length = 20,
        error_messages = { 'required':'用户名不能为空','min_lenght':'用户名长度不能小于4个字符','max_length':'用户名长度不能大于20个字符'}
    )
    password = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length = 12,
        max_length = 32,
        error_messages = {
            'requeird':'用户名不能为空',
            'invalid' : '密码必须保护数字,字母,特殊字符',
            'min_length' : "密码长度不能小于8个字符",
            'max_length' : "密码长度不能大于32个字符"
        }
    )

class BaseForm(BasebaseForm,django_forms.Form):
    hostname = django_fields.CharField(
        error_messages = {
            'requeired': '服务器名不能为空'
        }
    )
    ext_ip = django_fields.GenericIPAddressField(
        error_messages = {
            'requeired' : 'ext_ip is not null'
    }
    )
    int_ip = django_fields.GenericIPAddressField(
        error_messages = {
            'required' : 'int_ip is not null'
        }
    )
