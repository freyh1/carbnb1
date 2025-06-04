from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

from api.models import User, Car, Location

admin.site.register(User, UserAdmin)
admin.site.register(Car, ModelAdmin)
admin.site.register(Location, ModelAdmin)
