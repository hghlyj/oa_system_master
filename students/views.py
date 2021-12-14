import json
import os

import django_filters
from django.conf import settings
from django.http import FileResponse

from django_filters import rest_framework as filters
from openpyxl import load_workbook
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from register.models import Department, AdminUser
from students.models import Class_a, Student
from course.models import CoursePlan,RollCall
from students.serializers import ClassSerializer,StudentSerializer,StudentSerializerw



class ClassFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Class_a
        fields = []


class ClassView(ModelViewSet):
    queryset = Class_a.objects.all()#查询集
    serializer_class = ClassSerializer #序列化器

    # 指定使用 django-filter进行过滤查询
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class =ClassFilter

    @action(methods=['get'], detail=False)
    def filter_cls(self, request):
        id = request.query_params.get('id')
        if id:
            queryset = Class_a.objects.filter(college=id)
        ser = self.get_serializer(queryset, many=True)
        return Response(ser.data)


    #获取班级人数(教室号)
    def list(self, request, *args, **kwargs):
        # print(request.query_params.get('page'))
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        list = CoursePlan.objects.all()
        list2=[]
        for k in list:
            list2.append(k)
        if page is not None:
            for i in page:
                for w in list2:
                    if(i.id == w.classid.id):
                        i.room_number = w.room_number.number
                        i.teaching_time = w.teaching_time.id
                        i.class_time=w.class_time
                        i.course_plan=w.id
                        i.teacher=w.lecturer.id
                number = len(Student.objects.filter(cls=i.id))
                i.number = number
            serializer = self.get_serializer(page, many=True)
            print(serializer)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains')
    market = django_filters.CharFilter(lookup_expr='contains')
    dormnumber = django_filters.CharFilter(lookup_expr='contains')
    class Meta:
        model = Student
        fields = ['sex', 'cls']


def download_excel_temp(request):
    response = FileResponse(
        open(settings.EXCEL_FIEL_PATH + '/学生信息模板.xlsx', 'rb'))
    #用户点击下载链接之后 下载的文件的 文件名
    file_name='振涛教育-学生信息统计模板.xlsx'
    #告诉浏览器响应内容的类型为 二进制文件
    response['Content-Type'] = 'application/octet-stream'

    file_name = 'attachment; filename=%s' % file_name
    response['Content-Disposition'] = file_name.encode('utf-8', 'ISO-8859-1')
    return response

class StudentView(ModelViewSet):
    queryset = Student.objects.all() #查询集
    serializer_class = StudentSerializer #指定序列化器

    #指定使用 django-filter进行过滤查询
    filter_backends = (filters.DjangoFilterBackend,)
    #指定自定义的过滤器
    filterset_class = StudentFilter
    def create(self, request, *args, **kwargs):
        self.serializer_class=StudentSerializerw
        return super(StudentView, self).create(request)

    def update(self, request, *args, **kwargs):
        self.serializer_class = StudentSerializerw
        return super(StudentView, self).update(request)
    def list(self, request, *args, **kwargs):
        page = int(request.query_params.get('page'))
        pagesize= int(request.query_params.get('page_size'))
        list = self.queryset.values()
        list2=[]
        for i in list:
            list2.append(i)
        for k in list2:
            cls = Class_a.objects.get(id=k['cls_id'])
            k['department']=Department.objects.get(id=cls.college_id).name
            k['clsname']=cls.name
            try:
                CoursePlan.objects.get(classid_id=cls.id)
                k['lecturer'] = AdminUser.objects.get(id=CoursePlan.objects.get(classid_id=cls.id).lecturer_id).name
                k['counsellor'] = AdminUser.objects.get(id=CoursePlan.objects.get(classid_id=cls.id).counsellor_id).name
                k['coursestate']='完成排课'
            except:
                k['coursestate'] = '暂未排课'
        total = len(list2)
        #先过滤后分页
        name= request.query_params.get('name')
        market = request.query_params.get('market')
        cls = request.query_params.get('cls')
        sex = request.query_params.get('sex')
        dormnumber = request.query_params.get('dormnumber')
        if name is not None:
            print(name,222)
        list3 = list2[(page-1)*pagesize:page*pagesize]
        data = {'data':list3,'count':total,'code':200}
        return Response(data)



    #批量删除
    @action(methods=['get'], detail=False)
    def delete_stu(self, request):
        ids = request.query_params.get('ids')
        Student.objects.filter(pk__in=json.loads(ids)).delete()
        return Response({'msg':'批量删除成功'})

    #批量上传数据
    @action(methods=['post'], detail=False)
    def uploadexcel(self, request):
        school_id = request.data.get('school')
        class_id = request.data.get('cls')
        file = request.FILES.get('stufile')
        ext = file.name.rsplit('.', maxsplit=1)[1]  # 截取文件的后缀名
        filename = 'department_' + str(school_id) + '_cls_' + str(class_id) + '.' + ext
        filepath = settings.EXCEL_FIEL_PATH + filename

        with open(filepath, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        # 定义excel表中 每一列的值与数据表字段的映射关系 例如：excel第一列值对应数据表中的name字段值...
        excel_field = ('name','idcardnumber','anewconunt','score',  'sex', 'phone', 'family_phone', 'relations', 'address', 'dormnumber',
                       'bednumber', 'market','cls')
        wb = load_workbook(filename=filepath)  # 加载excel文件
        ws = wb.active  # 获取excel文件中的第一张表
        student_obj_list = []  # 定义学生对象（已经填充好数据）列表
        excel_rows = list(ws.rows)  # 获取表中的所有行 并转化成列表
        excel_rows.pop(0)  # 排除第一行的文档标题
        classobj = Class_a.objects.get(pk=class_id)
        idcard_list = []  # 文件中所有学生的身份证号
        # 从第二行开始读取 每一列中的值
        for row in excel_rows[0:-1]:
            obj = Student()  # 定义一个空的学生对象
            obj.cls = classobj  # 设置每个学生的班级id
            obj_attr = obj.__dict__  # 以字典的形式获取学生对象的属性信息（字典：{属性名:属性值...}）
            # 遍历数据行中的每一列 column
            for i, column in enumerate(row):
                if i == len(excel_field):
                    break  # 固定列数
                if column.value is None:
                    return Response({'error': '存在为空的单元格！' + str(column)})
                attr_name = excel_field[i]  # 根据列的下标获取对应的数据表字段
                if attr_name == 'idcardnumber':
                    idcard_list.append(column.value)
                obj_attr[attr_name] = column.value  # 根据表字段（对应的是StudentInfo模型所产生的对象的属性）对 对象属性进行赋值
            student_obj_list.append(obj)  # 将构造好的学生信息对象 插入到列表中
        exist_students = Student.objects.filter(idcardnumber__in=idcard_list).values()
        if exist_students:
            exist_students_id = ','.join([i.get('idcardnumber') for i in exist_students])
            return Response({'error': '已存在身份证号相同学生：' + exist_students_id})

        result = Student.objects.bulk_create(student_obj_list)  # 一次性插入到数据表
        if result:
            os.remove(filepath)
            return Response({'success': '成功'})
        return Response({'error': '导入失败！'})

#获取学生的点名信息
    def getStudentsRollCall(self,request):
        #获取班级id
        class_id=request.query_params.get('cls_id')
        #获取原课节日期
        class_date=request.query_params.get('class_date')
        #获取课节
        class_section=request.query_params.get('class_section')
        try:
            rc=RollCall.objects.get(class_section=class_section,class_date=class_date)
            data={}
            data['normal']=StudentSerializer(Student.objects.filter(idcardnumber__in=rc.normal.split(',')),many=True).data
            data['cut_classes']=StudentSerializer(Student.objects.filter(idcardnumber__in=rc.cut_classes.split(',')),many=True).data
            data['leave']=StudentSerializer(Student.objects.filter(idcardnumber__in=rc.leave.split(',')),many=True).data
            return Response(data)
        except:
            # 根据班级id 获取所有的学生信息
            students = Student.objects.filter(cls_id=class_id)
            ser=StudentSerializer(students,many=True)
            return Response(ser.data)