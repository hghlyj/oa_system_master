# Generated by Django 3.2 on 2021-12-14 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardedMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='加分原因')),
                ('Marks', models.CharField(max_length=20, verbose_name='加分')),
                ('create_data', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('update_data', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
            ],
            options={
                'db_table': 'Awarded_Marks',
            },
        ),
        migrations.CreateModel(
            name='Disciplinetype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='违纪类型')),
                ('content', models.TextField(null=True, verbose_name='类型描述内容')),
            ],
            options={
                'db_table': 'Discipline_Type',
            },
        ),
        migrations.CreateModel(
            name='Scoremethods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='管理方式')),
                ('content', models.TextField(null=True, verbose_name='简介')),
            ],
            options={
                'db_table': 'Score_Methods',
            },
        ),
        migrations.CreateModel(
            name='SubtractMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='违纪内容')),
                ('Marks', models.CharField(max_length=20, null=True, verbose_name='扣分')),
                ('expel', models.BooleanField(null=True, verbose_name='是否构成开除')),
                ('remark', models.TextField(null=True, verbose_name='备注')),
                ('create_data', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('update_data', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('Disciplinetype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentScore.disciplinetype')),
            ],
            options={
                'db_table': 'Subtract_Marks',
            },
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='姓名')),
                ('sex', models.BooleanField()),
                ('idcardnumber', models.CharField(max_length=60, verbose_name='身份证')),
                ('depar', models.CharField(max_length=60, verbose_name='学院')),
                ('cls', models.CharField(max_length=60, verbose_name='班级')),
                ('lecturer', models.CharField(max_length=60, verbose_name='讲师')),
                ('counsellor', models.CharField(max_length=60, verbose_name='导员')),
                ('dormnumber', models.IntegerField(verbose_name='宿舍号')),
                ('bednumber', models.IntegerField(verbose_name='床位号')),
                ('address', models.CharField(max_length=60, verbose_name='家庭住址')),
                ('market', models.CharField(max_length=200, verbose_name='市场部')),
                ('state', models.BooleanField(verbose_name='加减分?')),
                ('content', models.CharField(max_length=200, verbose_name='加减分项')),
                ('Marks', models.IntegerField(verbose_name='分数')),
                ('avatar', models.FileField(default='static/ScoreMarksImg/default.png', null=True, upload_to='static/ScoreMarksImg', verbose_name='违纪图片')),
                ('data', models.DateField(verbose_name='违纪(获奖)日期')),
                ('course', models.CharField(max_length=100, null=True, verbose_name='课节')),
                ('fdyoppose', models.CharField(max_length=100, null=True, verbose_name='申诉原因')),
                ('create_data', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('update_data', models.DateTimeField(auto_now=True, null=True, verbose_name='审核时间')),
                ('status', models.IntegerField(default=0, verbose_name='0未批，1.承认，2.不承认,3.待审批,4.审批通过')),
                ('disciplinetype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentScore.disciplinetype', verbose_name='违纪类型')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.student')),
            ],
            options={
                'db_table': 'student_score',
            },
        ),
        migrations.CreateModel(
            name='PutIntoEffect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pid', models.IntegerField()),
                ('putintoeffect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentScore.scoremethods')),
            ],
            options={
                'db_table': 'Put_Into_Effect',
            },
        ),
    ]
