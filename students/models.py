from django.db import models

from register.models import Department



class Class_a(models.Model):
    name=models.CharField(max_length=10,verbose_name='班级的名称')
    college=models.ForeignKey(to=Department,on_delete=models.CASCADE,verbose_name='班级所属学院')
    #
    # stage=models.CharField(max_length=60,verbose_name='现处阶段')
    # room_number=models.IntegerField(verbose_name='教室号')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'class'
        ordering = ['-id']

class Student(models.Model):
    name = models.CharField(max_length=10,verbose_name='学生姓名')
    idcardnumber = models.CharField(max_length=20, verbose_name='身份证号', unique=True)
    sex = models.IntegerField()
    phone=models.CharField(max_length=11)
    family_phone=models.CharField(max_length=11,verbose_name='家长手机号')

    anewconunt=models.IntegerField('重修次数',null=True)
    score = models.IntegerField('综合积分',null=True)

    relations=models.CharField(max_length=30,verbose_name='亲子关系')
    address=models.CharField(max_length=100,verbose_name='学生地址')
    dormnumber=models.IntegerField(verbose_name='宿舍号')
    bednumber=models.IntegerField(verbose_name='床号')
    market=models.CharField(max_length=30,verbose_name='市场部')
    cls=models.ForeignKey(to=Class_a,on_delete=models.SET_NULL,null=True, related_name='cls')


    def __str__(self):
        return self.name
    class Meta:
        db_table='student_info'


