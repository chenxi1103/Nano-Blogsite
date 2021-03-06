# Generated by Django 2.1 on 2018-10-22 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0003_remove_post_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='lastName',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tel',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='whatsUp',
            field=models.CharField(max_length=42),
        ),
    ]
