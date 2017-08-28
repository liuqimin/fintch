from django.contrib import admin
from base import models
# Register your models here.

admin.site.register(models.Base)
admin.site.register(models.Project)
admin.site.register(models.Service)
admin.site.register(models.UserProfile)
