# Generated by Django 3.0.8 on 2020-09-22 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_merge_20200922_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
