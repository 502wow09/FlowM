# Generated by Django 3.2.6 on 2021-08-31 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20210830_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='director',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='owner_movie',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='owner_user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='owner',
        ),
    ]
