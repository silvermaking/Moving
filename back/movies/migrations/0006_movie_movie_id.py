# Generated by Django 3.2.3 on 2021-11-18 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20211118_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]