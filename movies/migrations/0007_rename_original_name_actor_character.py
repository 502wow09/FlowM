# Generated by Django 3.2.6 on 2021-09-01 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_movie_keyword_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actor',
            old_name='original_name',
            new_name='character',
        ),
    ]