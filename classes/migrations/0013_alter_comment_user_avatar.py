# Generated by Django 4.1.3 on 2023-05-27 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0012_alter_comment_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_avatar',
            field=models.ImageField(default='users/user-avatar.png', upload_to='users/'),
        ),
    ]
