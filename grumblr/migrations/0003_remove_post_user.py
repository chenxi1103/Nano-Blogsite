# Generated by Django 2.1 on 2018-10-22 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_remove_post_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]
