from django.db import models
from register.models import AdminUser,Department
from students.models import Class_a
from django.utils import timezone

#教学周期

class TeachingTime(models.Model):
    title=models.CharField(max_length=30)
    starttime=models.DateTimeField()
    endtime=models.DateTimeField()
    am_class=models.TextField('上午上课日期',max_length=1000,null=True)
    pm_class=models.TextField('下午午上课日期',max_length=1000,null=True)
    no_class=models.TextField('没课日期',max_length=1000,null=True)
    is_start = models.BooleanField(default=False, verbose_name='是否开始')
    class Meta:
        db_table='teaching_time'
        ordering = ['-id']

#学院教研室（阶段）
class CollegeStage(models.Model):
    name=models.CharField(max_length=30)
    college=models.ForeignKey(to=Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table='college_stage'
        ordering = ['-id']

#课程体系表
class Courses(models.Model):
    name=models.CharField('课程名称',max_length=30)
    school=models.ForeignKey(to=Department,on_delete=models.CASCADE)
    stage=models.CharField(max_length=60)#课程阶段
    college_stage = models.ForeignKey(to=CollegeStage, on_delete=models.CASCADE)  # 学院阶段（专业、专高、实训）
    sort=models.IntegerField()
    version=models.CharField(max_length=10)

    class Meta:
        db_table = 'courses'
        ordering = ['sort']


#教室表
class Classroom(models.Model):
    department = models.ForeignKey(to=Department,on_delete=models.CASCADE)
    address=models.CharField('教室地址',max_length=50)
    number=models.CharField('教室号',max_length=30)
    class Meta:
        db_table='classroomclass'


#排课表
class CoursePlan(models.Model):
    teaching_time=models.ForeignKey(to=TeachingTime,on_delete=models.CASCADE)
    lecturer=models.ForeignKey(to=AdminUser,on_delete=models.SET_NULL,null=True,blank=True,related_name='js')
    counsellor=models.ForeignKey(to=AdminUser,on_delete=models.SET_NULL,null=True,blank=True,related_name='fdy')
    room_number=models.OneToOneField(to=Classroom,on_delete=models.SET_NULL,null=True,blank=True,related_name='jsh')
    class_time=models.CharField(max_length=1000)
    course=models.ForeignKey(to=Courses,on_delete=models.SET_NULL,null=True)
    classid= models.OneToOneField(to=Class_a,on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table='course_plan'

#调/代课表
class AdjustClassTime(models.Model):
    # cls = models.ForeignKey(to=Class, on_delete=models.CASCADE)
    course_plan=models.ForeignKey(to=CoursePlan,on_delete=models.CASCADE)
    original_date=models.DateField()
    change_date=models.DateField()
    createtime=models.DateTimeField(auto_now_add=True)
    teacher=models.ForeignKey(to=AdminUser,on_delete=models.CASCADE)
    change_type=models.BooleanField()
    change_teacher=models.ForeignKey(to=AdminUser,on_delete=models.CASCADE,related_name='change_teacher')
    state=models.IntegerField(default=0)
    class Meta:
        db_table='adjust_class_time'

#调课课节映射
class AdjustClassMap(models.Model):
    act=models.ForeignKey(to=AdjustClassTime,on_delete=models.CASCADE)
    initial=models.CharField(max_length=50)
    final=models.CharField(max_length=50)
    is_take_effect = models.BooleanField(default=True)
    class Meta:
        db_table='adjust_class_map'

#点名表（课表）
class RollCall(models.Model):
    teaching_time = models.ForeignKey(to=TeachingTime, on_delete=models.CASCADE,verbose_name='教学周期')
    lecturer_id = models.IntegerField(verbose_name='讲师的id', null=True)
    class_id = models.IntegerField(verbose_name='班级id', null=True)
    act = models.ForeignKey(to=AdjustClassTime, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    course_plan = models.ForeignKey(to=CoursePlan, on_delete=models.CASCADE, null=True)

    department = models.CharField(max_length=80, verbose_name='部门信息')
    lecturer = models.CharField(max_length=30,verbose_name='讲师')
    counsellor = models.CharField(max_length=30,verbose_name='导员')
    class_name = models.CharField(max_length=30,verbose_name='班级名称')
    room_number = models.CharField(verbose_name='教室号', max_length=30)
    class_date=models.DateField(verbose_name='课程日期')
    class_section = models.CharField(max_length=10,verbose_name='课节') #课节
    actual_date=models.DateField(verbose_name='实际的课程日期')
    actual_section=models.CharField(max_length=10,verbose_name='实际的课节')
    course = models.CharField(max_length=80,verbose_name='课程信息')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time=models.DateTimeField(verbose_name='最后一次点名时间',null=True,auto_now=True)
    normal=models.TextField(verbose_name='正常出勤的学生的身份证号')
    cut_classes=models.TextField(verbose_name='旷课的学生的身份证号',null=True,blank=True)
    leave=models.TextField(verbose_name='请假',null=True,blank=True)
    late=models.TextField(verbose_name='迟到',null=True,blank=True)
    state=models.BooleanField(default=False,verbose_name='是否点名')

    students_num = models.IntegerField(null=True, default=0, verbose_name='总人数')
    attendance_num = models.IntegerField(null=True, default=0, verbose_name='实际出勤人数')
    college_stage = models.ForeignKey(to=CollegeStage, null=True, on_delete=models.CASCADE, verbose_name='阶段的id')
    class Meta:
        db_table = 'roll_call'



