# Generated by Django 3.2 on 2021-12-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentScore', '0002_alter_studentscore_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentscore',
            name='avatar',
            field=models.FileField(null=True, upload_to='static/ScoreMarksImg', verbose_name='违纪图片'),
        ),
    ]
