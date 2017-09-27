from django import forms
from .models import Asset
from django.forms import fields as django_fields
from django.forms import widgets
from django.utils.safestring import mark_safe

class Asset_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(Asset_form, self).clean()
        value = cleaned_data.get('sn')
       # ipaddress_value = cleaned_data.get('ipaddress')
        try:
            Asset.objects.get(sn=value)
            self._errors['sn']=self.error_class(["%s的信息已经存在" % value])
        except Asset.DoesNotExist:
            pass

        return cleaned_data
    class Meta:
        model = Asset
        exclude =('ni',)

        widgets = {
            'sn': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_model': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': ' form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'macaddress': forms.TextInput(attrs={'class': 'form-control'}),
            'ipaddress': forms.TextInput(attrs={'class': 'form-control'}),
        }

    @property
    def jsonlist(self):
        '''
        ## error错误 table显示
        :return:
        '''
        if self.errors:
            data =self.errors.as_data()
            result = ''
            print(Asset._meta.get_field('sn').__dict__['verbose_name'])
            for error_key,error_value in data.items():

                result += '<tbody><tr><td>{}</td><td>{}</td></tr></tbody>'.format(Asset._meta.get_field(error_key)\
                    .__dict__['verbose_name'],error_value[0].messages[0])

            result = '<table class="layui-table"><thead><tr><th>字段</th><th>错误内容</th></tr>'+result+\
                     '</tbody></table>'

        return mark_safe(result)



