# Generated by Django 4.1.3 on 2023-05-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customer_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(default='users/user-avatar.png', upload_to='users/'),
        ),
    ]
