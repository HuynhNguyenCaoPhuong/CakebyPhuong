from django.contrib import admin
from . import models

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering = ['user']
    list_display = ['user', 'facebook', 'tel', 'address']
    search_fields = ['user__username']
