# Generated by Django 3.0.7 on 2020-06-10 10:45

from django.db import migrations, models
import userManagement.models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='/static\\img\\baseAvatar.png', upload_to=userManagement.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='user_<property object at 0x0400E988>@default.com', max_length=254, unique=True),
        ),
    ]