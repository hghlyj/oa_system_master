from django.db import models

# Create your models here.

#     Name: 	String	姓名（人像面）
#     Sex:	String	性别（人像面）
#     Nation:	String	民族（人像面）
#     Birth:	String	出生日期（人像面）
#     Address:	String	地址（人像面）
#     IdNum:	String	身份证号（人像面）
#     Authority:	String	发证机关（国徽面）
#     ValidDate:	String	证件有效期（国徽面）
class Schoolroll(models.Model):
    Name=models.CharField('姓名',max_length=60)
    Sex=models.BooleanField('性别')
    Birth = models.DateField('出生日期')
    Nation=models.CharField('民族',max_length=60)
    Address=models.CharField('地址',max_length=60)
    IdNum = models.CharField('身份证号',max_length=100)
    Authority = models.CharField('发证机关',max_length=100)
    ValidDate = models.CharField('证件有效期',max_length=100)

    class Meta:
        db_table = 'school_roll'
        ordering = ('-id',)