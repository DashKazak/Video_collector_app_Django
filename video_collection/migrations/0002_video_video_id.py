# Generated by Django 4.0.4 on 2022-04-21 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_id',
            field=models.CharField(default=1, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]