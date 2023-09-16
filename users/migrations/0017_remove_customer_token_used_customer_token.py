# Generated by Django 4.1.3 on 2023-06-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_customer_token_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='token_used',
        ),
        migrations.AddField(
            model_name='customer',
            name='token',
            field=models.CharField(default=None, max_length=255, unique=True),
        ),
    ]
