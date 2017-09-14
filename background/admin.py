from django.contrib import admin
from background import models
# Register your models here.

admin.site.register(models.Blog)
admin.site.register(models.AriticleDetail)
admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
admin.site.register(models.UpDown)