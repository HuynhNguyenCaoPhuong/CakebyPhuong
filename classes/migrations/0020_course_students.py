# Generated by Django 4.1.3 on 2023-06-02 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0019_paidcourses'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.IntegerField(default=0),
        ),
    ]
