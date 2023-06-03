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
    

@admin.register(models.PaidCourses)
class PaidCoursesAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ['created', 'username', 'course']
    search_fields = ['username__istartswith']
    list_editable = ['username', 'course']
    list_filter = ['created']
    

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
    

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_first_name', 'content']
    list_filter = ['created_at']
    search_fields = ['user_first_name__istartswith']
    list_per_page = 10

    @admin.display(ordering='created_at')
    def date_status(self, comment):
        if comment.created_at == 0:
            return 'No'
        return 'Yes'
    

@admin.register(models.Blogcomment)
class BlogcommentAdmin(admin.ModelAdmin):
    list_display = ['user_first_name', 'content']
    list_filter = ['created_at']
    search_fields = ['user_first_name__istartswith']
    list_per_page = 10

    @admin.display(ordering='created_at')
    def date_status(self, blogcomment):
        if blogcomment.created_at == 0:
            return 'No'
        return 'Yes'
    

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'message']
    list_filter = ['id']
    search_fields = ['name__istartswith']
    list_per_page = 10

    @admin.display(ordering='id')
    def date_status(self, contact):
        if contact.id == 0:
            return 'No'
        return 'Yes'
        