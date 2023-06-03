from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=30)
    address = models.TextField()
    facebook = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='users/', default='user-avatar.png', null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=255, unique=True, default=None, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username}'
    
    class Meta:
        db_table = u'customers'