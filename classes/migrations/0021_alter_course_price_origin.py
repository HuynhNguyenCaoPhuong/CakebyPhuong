# Generated by Django 4.1.3 on 2023-06-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0020_course_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price_origin',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]