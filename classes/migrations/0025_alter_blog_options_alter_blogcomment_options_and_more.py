# Generated by Django 4.1.3 on 2023-06-11 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0024_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('-public_day',), 'verbose_name_plural': 'Blog chia sẻ mẹo'},
        ),
        migrations.AlterModelOptions(
            name='blogcomment',
            options={'verbose_name_plural': 'Comment trong blog'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': 'Comment trong khóa học'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name_plural': 'Tin nhắn liên hệ'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-public_day',), 'verbose_name_plural': 'Tất cả khóa học'},
        ),
        migrations.AlterModelOptions(
            name='paidcourses',
            options={'verbose_name_plural': 'Danh sách học viên mua khóa học'},
        ),
    ]