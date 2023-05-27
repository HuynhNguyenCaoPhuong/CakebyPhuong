from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'slug']
    search_fields = ['name']
    

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display = ['name', 'price', 'price_origin', 'category']
    list_filter = ['public_day', 'category']
    list_editable = ['price', 'price_origin']
    search_fields = ['name__istartswith']
    list_per_page = 10

    def category_name(self, course):
        return course.category.name

    @admin.display(ordering='viewed')
    def viewed_status(self, course):
        if course.viewed == 0:
            return 'No'
        return 'Yes'
    

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['public_day']
    search_fields = ['name__istartswith']
    list_per_page = 10

    @admin.display(ordering='public_day')
    def date_status(self, blog):
        if blog.public_day == 0:
            return 'No'
        return 'Yes'