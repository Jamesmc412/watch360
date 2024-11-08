# Generated by Django 5.1.2 on 2024-11-05 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to='avatars/'),
        ),
    ]
