# Generated by Django 4.0 on 2021-12-25 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]