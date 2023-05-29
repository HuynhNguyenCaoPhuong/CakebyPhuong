from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# from users.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    img = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png')
    courses = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def update_courses_count(self):
        self.courses = Course.objects.filter(category=self).count()
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=500)
    price = models.FloatField(default=0.0)
    price_origin = models.FloatField(null=True)
    video = models.CharField(max_length=500, null=True, blank=True)
    image_course = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png')
    is_free = models.BooleanField(default=True)
    describe = RichTextUploadingField(null=True, blank=True)
    public_day = models.DateTimeField(auto_now_add=True)
    viewed = models.IntegerField(default=0)
    vote = models.FloatField(null=True, blank=True, default=5)
    star = models.TextField(default='<small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small>')

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'name': self.name,
            'describe': self.describe,
            'price': str(self.price), 
        }
    
    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)
        self.category.update_courses_count()

    class Meta:
        ordering = ('-public_day',)


class Blog(models.Model):
    name = models.CharField(max_length=500)
    video = models.CharField(max_length=500, null=True, blank=True)
    image_blog = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png')
    describe = RichTextUploadingField(null=True, blank=True)
    public_day = models.DateTimeField(auto_now_add=True)
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'name': self.name,
            'describe': self.describe,
        }

    class Meta:
        ordering = ('-public_day',)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_first_name = models.CharField(max_length=255, null=True, blank=True)
    user_last_name = models.CharField(max_length=255, null=True, blank=True)
    user_avatar = models.ImageField(upload_to='users/', default='user-avatar.png')
    image = models.ImageField(upload_to='comments/', null=True, blank=True)

    def __str__(self):
        return self.content
    

class Blogcomment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_first_name = models.CharField(max_length=255, null=True, blank=True)
    user_last_name = models.CharField(max_length=255, null=True, blank=True)
    user_avatar = models.ImageField(upload_to='users/', default='user-avatar.png')
    image = models.ImageField(upload_to='comments/', null=True, blank=True)

    def __str__(self):
        return self.content

    
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
    
