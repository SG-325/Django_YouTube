# Generated by Django 3.1.3 on 2020-12-05 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('download_app', '0003_newmp3_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newmp3',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
