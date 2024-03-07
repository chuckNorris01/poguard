from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'role')
    list_display_links = ('id', 'email', 'name', 'role')
    list_filter = ('id', 'email', 'name', 'role')