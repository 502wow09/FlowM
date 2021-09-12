# Generated by Django 3.2.6 on 2021-09-12 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_rename_original_name_actor_character'),
    ]

    operations = [
        migrations.AlterField(
            model_name='similar',
            name='recommand_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie'),
        ),
        migrations.AlterField(
            model_name='similar',
            name='search_id',
            field=models.IntegerField(default=0),
        ),
    ]