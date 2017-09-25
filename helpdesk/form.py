from django import forms
from .models import Asset



class Asset_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(Asset_form, self).clean()
        value = cleaned_data.get('name')
        try:
            Asset.objects.get(name=value)
            self._errors['sn']=self.error_class(["%s的信息已经存在" % value])
        except Asset.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = Asset
        exclude = ("ni",)
