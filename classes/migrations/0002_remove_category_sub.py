# Generated by Django 4.1.3 on 2023-05-23 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='sub',
        ),
    ]
