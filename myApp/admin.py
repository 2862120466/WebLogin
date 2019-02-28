from django.contrib import admin
from .models import User,ConfirmString
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','password','email','sex','c_time','has_confirmed']
    list_filter = ['name']
    list_per_page = 5
    search_fields = ['name']

@admin.register(ConfirmString)
class UserAdmin(admin.ModelAdmin):
    list_display = ['code','user','c_time']
    list_filter = ['user']
    list_per_page = 5
    search_fields = ['user']