# Generated by Django 4.1.3 on 2023-05-27 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customer_facebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(default='user-avatar.png', upload_to='media/users'),
        ),
    ]
