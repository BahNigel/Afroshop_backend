# Generated by Django 5.1.3 on 2024-12-04 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_delete_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
