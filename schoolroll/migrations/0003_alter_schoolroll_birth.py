# Generated by Django 3.2 on 2021-12-19 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolroll', '0002_auto_20211219_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolroll',
            name='Birth',
            field=models.DateField(verbose_name='出生日期'),
        ),
    ]
