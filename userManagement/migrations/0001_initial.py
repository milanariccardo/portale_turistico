# Generated by Django 3.0.7 on 2020-06-09 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userManagement.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='/static/img/baseAvatar.png', upload_to=userManagement.models.user_directory_path)),
                ('email', models.EmailField(default='user_<property object at 0x7f2509aa4278>@default.com', max_length=254, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
