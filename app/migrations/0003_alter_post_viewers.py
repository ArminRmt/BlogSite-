# Generated by Django 4.0 on 2021-12-23 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_post_details_post_title2_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='viewers',
            field=models.CharField(default='0', max_length=100, null=True),
        ),
    ]
