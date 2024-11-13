# Generated by Django 5.1.2 on 2024-11-13 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchapp', '0002_alter_onlinestatus_video_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinestatus',
            name='video_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='watchapp.youtubedata'),
        ),
    ]
