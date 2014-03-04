from django.contrib import admin
from sharetools.models import Shed
from sharetools.models import Tool
from sharetools.models import UserToolShareProfile

# Register your models here.

admin.site.register(Shed)
admin.site.register(Tool)
admin.site.register(UserToolShareProfile)
