from django.contrib import admin
from sharetools.models import Shed, Tool, UserProfile, ShareContract

# Register your models here.

admin.site.register(Shed)
admin.site.register(Tool)
admin.site.register(UserProfile)
admin.site.register(ShareContract)
