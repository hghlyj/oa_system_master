
from django.db import models
from students.models import Student


#积分管理方法
class Scoremethods(models.Model):
    name=models.CharField('管理方式',max_length=200)
    content=models.TextField('简介',null=True)

    class Meta:
        db_table = 'Score_Methods'


#获取每一项类型的具体内容描述
class PutIntoEffect(models.Model):
    putintoeffect=models.ForeignKey(to=Scoremethods, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    pid = models.IntegerField()

    class Meta:
        db_table = 'Put_Into_Effect'

#记入加分项
class AwardedMarks(models.Model):
    content = models.CharField('加分原因', max_length=200)
    Marks = models.CharField('加分',max_length=20)
    # remark = models.TextField('备注')
    create_data = models.DateTimeField('添加日期', auto_now_add=True, auto_now=False)
    update_data = models.DateTimeField('修改时间', auto_now_add=False, auto_now=True, null=True)
    # pid = models.IntegerField()

    class Meta:
        db_table = 'Awarded_Marks'

#违纪分类及其描述
class Disciplinetype(models.Model):
    name=models.CharField('违纪类型',max_length=200)
    content = models.TextField('类型描述内容',null=True)
    class Meta:
        db_table = 'Discipline_Type'

#记入减分项
class SubtractMarks(models.Model):
    Disciplinetype = models.ForeignKey(to=Disciplinetype,on_delete=models.SET_NULL,null=True)
    content = models.CharField('违纪内容',max_length=200)
    Marks=models.CharField('扣分',max_length=20,null=True)
    expel=models.BooleanField('是否构成开除',null=True)
    remark = models.TextField('备注',null=True)
    create_data = models.DateTimeField('添加日期', auto_now_add=True, auto_now=False)
    update_data = models.DateTimeField('修改时间', auto_now_add=False, auto_now=True, null=True)

    class Meta:
        db_table='Subtract_Marks'


# 学生id   学生姓名  学院  班级  讲师  导员  加减分项   分数   图片  日期  课节    是否承认
class StudentScore(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.SET_NULL, null=True)
    name = models.CharField('姓名',max_length=60)
    sex = models.BooleanField()
    idcardnumber=models.CharField('身份证',max_length=60)
    depar=models.CharField('学院',max_length=60)
    cls = models.CharField('班级',max_length=60)
    lecturer=models.CharField('讲师',max_length=60)
    counsellor=models.CharField('导员',max_length=60)
    dormnumber=models.IntegerField('宿舍号')
    bednumber=models.IntegerField('床位号')
    address=models.CharField('家庭住址',max_length=60)
    market=models.CharField('市场部',max_length=200)

    state = models.BooleanField('加减分?')
    disciplinetype= models.ForeignKey(to=Disciplinetype,on_delete=models.SET_NULL,null=True,verbose_name='违纪类型')
    content=models.CharField('加减分项',max_length=200)
    Marks=models.IntegerField('分数')
    avatar=models.FileField(upload_to='static/ScoreMarksImg', default='static/ScoreMarksImg/default.png', verbose_name='违纪图片',null=True)
    data=models.DateField('违纪(获奖)日期',auto_now_add=False,auto_now=False)
    course=models.CharField('课节',max_length=100,null=True)
    fdyoppose=models.CharField('申诉原因',max_length=100,null=True)

    create_data=models.DateTimeField('提交时间',auto_now_add=True,auto_now=False)
    update_data=models.DateTimeField('审核时间',auto_now_add=False,auto_now=True,null=True)
    status=models.IntegerField('0未批，1.承认，2.不承认,3.待审批,4.审批通过',default=0)
    class Meta:
        db_table = 'student_score'

# class FilesModel(models.Model):
#     file = models.FileField(upload_to='static/ScoreMarksImg')
#
#     class Meta:
#         db_table = 'files_storage'
#         ordering = ['-id']

