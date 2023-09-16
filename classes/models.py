from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from users.models import Customer
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

    class Meta:
        verbose_name_plural = "Danh mục bánh"


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=500)
    price = models.FloatField(default=0.0)
    price_origin = models.FloatField(null=True, default=0.0)
    video = models.CharField(max_length=500, null=True, blank=True)
    image_course = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png')
    is_free = models.BooleanField(default=True)
    describe = RichTextUploadingField(null=True, blank=True)
    public_day = models.DateTimeField(auto_now_add=True)
    time = models.CharField(max_length=100, default='10 phút')
    students = models.IntegerField(default=0)
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
    
    def update_students_count(self):
        self.students = PaidCourses.objects.filter(course=self).count()
        self.save()
    
    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)
        self.category.update_courses_count()

    class Meta:
        ordering = ('-public_day',)
        verbose_name_plural = "Khóa học bánh"


class PaidCourses(models.Model):
    username = models.CharField(max_length=50, null=False)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        user = User.objects.get(username=self.username)
        customer = Customer.objects.get(user=user)
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.tel = customer.tel
        self.address = customer.address
        super(PaidCourses, self).save(*args, **kwargs)
        self.course.update_students_count()

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural = "Danh sách user đã thanh toán"


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
        verbose_name_plural = "Blog chia sẻ mẹo"


class Comment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
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
    
    class Meta:
        verbose_name_plural = "Comment trong khóa học"
    
    

class Blogcomment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
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
    
    class Meta:
        verbose_name_plural = "Comment trong blog"

    
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Tin nhắn liên hệ"
    
