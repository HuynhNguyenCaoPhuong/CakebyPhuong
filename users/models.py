from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    tel = models.CharField(max_length=30)
    address = models.TextField()
    facebook = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='users/', default='user-avatar.png', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        db_table = u'customers'