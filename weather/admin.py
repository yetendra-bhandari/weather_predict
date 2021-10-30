from django.contrib import admin

from .models import User, Data


class DataAdmin(admin.ModelAdmin):
    list_display = ['user', 'csvname']


admin.site.register(Data, DataAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


admin.site.register(User, UserAdmin)
