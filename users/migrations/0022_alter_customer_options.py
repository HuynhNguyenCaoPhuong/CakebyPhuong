# Generated by Django 4.1.3 on 2023-06-11 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_customer_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name_plural': 'Thông tin thêm của thành viên'},
        ),
    ]