from django.contrib import admin
from sharetools.models import Location, Asset, UserProfile, ShareContract, Address, Asset_Type, Membership

# Register your models here.

admin.site.register(Address)
admin.site.register(Location)
admin.site.register(Asset_Type)
admin.site.register(Asset)
admin.site.register(UserProfile)
admin.site.register(ShareContract)
admin.site.register(Membership)
