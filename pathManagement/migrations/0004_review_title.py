# Generated by Django 3.0.6 on 2020-06-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathManagement', '0003_auto_20200612_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default='Titolo prova', max_length=255),
            preserve_default=False,
        ),
    ]
