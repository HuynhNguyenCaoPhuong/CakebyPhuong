# Generated by Django 4.1.3 on 2023-06-03 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_customer_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='token',
            new_name='token_used',
        ),
    ]
