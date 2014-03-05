from django.contrib import admin
<<<<<<< HEAD
from sharetools.models import Shed, Tool, UserProfile, ShareContract
=======
from sharetools.models import Shed
from sharetools.models import Tool
from sharetools.models import UserToolShareProfile
>>>>>>> FETCH_HEAD

# Register your models here.

admin.site.register(Shed)
admin.site.register(Tool)
<<<<<<< HEAD
admin.site.register(UserProfile)
admin.site.register(ShareContract)
=======
admin.site.register(UserToolShareProfile)
>>>>>>> FETCH_HEAD
