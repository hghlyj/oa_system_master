from django.db import models
from django.contrib.auth.models import AbstractUser

#部门表
class Department(models.Model):
    name = models.CharField(max_length=33,verbose_name='部门名称',unique=True)
    label = models.BooleanField(verbose_name='是否是学院')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'
        ordering = ('-id',)

#角色表
class Role(models.Model):
    role_name=models.CharField(max_length=10,verbose_name='角色、职位')
    department=models.ForeignKey(to=Department,on_delete=models.CASCADE,verbose_name='部门id')
    level=models.IntegerField(verbose_name='岗位级别')
    duty = models.CharField(verbose_name='岗位职责',max_length=50,null=True)

    class Meta:
        db_table = 'role'
        ordering = ('-id',)


#用户表
class AdminUser(AbstractUser):
    phone = models.CharField(max_length=11)
    Role = models.ManyToManyField(to=Role)
    name = models.CharField('姓名',max_length=100)
    # avatar = models.FileField(upload_to='static/img', default='static/img/default.png', null=True,verbose_name='头像')
    class Meta:
        db_table = 'adminuser'
        ordering = ('-id',)




