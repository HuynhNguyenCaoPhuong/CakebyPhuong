# Generated by Django 4.1.3 on 2023-05-30 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customer_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
