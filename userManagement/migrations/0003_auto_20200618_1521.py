# Generated by Django 3.0.7 on 2020-06-18 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0002_auto_20200617_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='user_<property object at 0x7f275855c408>@default.com', max_length=254, unique=True),
        ),
    ]
