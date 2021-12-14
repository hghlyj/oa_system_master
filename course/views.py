import copy
import itertools

from django.db.models import Sum, Q, Count
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from students.models import Class_a, Student
from .serializers import TeachingTimeSerializers, CoursePlanSerializers, \
    ClassroomSerializers, CoursesSerializers, AdjustClassTimeSerializers, UserCoursePlanSerializer, RollCallSerializer, \
    CollegeStageSerializer
from .models import TeachingTime, Courses, CoursePlan, Classroom, AdjustClassTime, AdjustClassMap, RollCall, \
    CollegeStage
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin
from register.models import AdminUser, Department

#教学周期视图
class TeachingTimes(ModelViewSet):
    queryset = TeachingTime.objects.all()
    serializer_class = TeachingTimeSerializers

    @action(methods=['get'], detail=False)
    def all(self, request):
        ser = self.get_serializer(self.get_queryset(), many=True)
        return Response(ser.data)

    def list(self, request, *args, **kwargs):
        queryinfo = request.query_params.get('queryinfo')
        if (queryinfo == 'nopaged' or queryinfo == 'activated' or queryinfo == 'current'):
            self.pagination_class = None
            if (queryinfo == 'activated'):
                # self.queryset = TeachingTime.objects.filter(starttime__gte=timezone.now())
                self.queryset = TeachingTime.objects.filter(endtime__gte=timezone.now())
            if (queryinfo == 'current'):
                self.queryset = TeachingTime.objects.filter(endtime__gt=timezone.now(), starttime__lte=timezone.now())

        return super(TeachingTimes, self).list(request)

    def getTeachingTime(self, request):
        queryinfo = request.query_params.get('queryinfo')
        if (queryinfo == 'current'):
             instance = get_object_or_404(TeachingTime, is_start=True)
             ser = self.get_serializer(instance)
             return Response(ser.data)
        self.pagination_class = None
        if (queryinfo == 'activated'):
            self.queryset = TeachingTime.objects.filter(endtime__gt=timezone.now())
        return self.list(request)
#学院课程阶段视图
class CollegeStageView(ModelViewSet):
    queryset = CollegeStage.objects.all()
    serializer_class = CollegeStageSerializer
    filter_fields = ('college_id',)
    def get_queryset(self):
        queryinfo=self.request.query_params.get('queryinfo')
        if(queryinfo=='nopaging'):
            self.pagination_class=None
        return self.queryset

#教室
class Classrooms(ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializers

    @action(methods=['get'], detail=False)
    def all(self, request):
        part = request.query_params.get('part')
        content = CoursePlan.objects.all()
        cls = Classroom.objects.all()
        list = []
        for k in cls:
            if k.department.name==part:
                for i in content:
                    if k.number == i.room_number.number:
                        k.classname=i.classid.name
                list.append(k)
        ser = self.get_serializer(list, many=True)
        return Response(ser.data)

#课程体系视图
class Coursess(ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializers

    @action(methods=['get'], detail=False)
    def all(self, request):
        part = request.query_params.get('part')
        q=[]
        for k in self.get_queryset():
            school = k.school.name
            if school==part:
                q.append(k)
        ser = self.get_serializer(q, many=True)
        return Response(ser.data)
    def list(self, request, *args, **kwargs):
        cls_id = request.query_params.get('class_id')
        if (cls_id):
            self.pagination_class = None  # 不分页
            try:
                cls = Class_a.objects.get(pk=cls_id)
                self.queryset = cls.school.courses_set.all()
            except:
                self.queryset = []
        return super(Coursess, self).list(request)
# 排课视图
class CoursePlans(ModelViewSet):
    queryset = CoursePlan.objects.all()
    serializer_class = CoursePlanSerializers

    @action(methods=['get'], detail=False)
    def all(self, request):
        ser = self.get_serializer(self.get_queryset(), many=True)
        return Response(ser.data)

class UserCoursePlanView(ViewSet):

    # 获取用户本月教学周期的排课信息
    def getCp(self, userId):
        try:
            # tc = TeachingTime.objects.get(starttime__lte=timezone.now(), endtime__gte=timezone.now())
            # cp = CoursePlan.objects.filter(teaching_time_id=tc.id, lecturer_id=userId)
            cp = CoursePlan.objects.filter( lecturer_id=userId)
            return cp
        except:
            return None

    def get(self, request):
        cp = self.getCp(request.user.id)
        if cp:
            ser = UserCoursePlanSerializer(cp, many=True)
            return Response(ser.data)
        return Response([])

    def validate(self, data, id):
        error_message = {}
        if not data.get('course_plan'):
            error_message['course_plan'] = '排课id course_plan 参数必须'
        change_type = data.get('change_type')
        if change_type is None:
            error_message['change_type'] = '调课类型change_type 参数是必须的'
        if not data.get('original_date'):
            error_message['original_date'] = '原上课日期 original_date 参数是必须的'

        original_class = data.get('original_class', [])
        if not original_class:
            error_message['original_class'] = '原课节 original_class 参数是必须的'

        if not data.get('change_date'):
            error_message['change_date'] = '调课日期 change_date 参数是必须的'

        from datetime import datetime
        changeTime = datetime.strptime(data['change_date'], '%Y-%m-%d')
        nowTimeStr = timezone.now().strftime("%Y-%m-%d")
        nowTime = datetime.strptime(nowTimeStr, '%Y-%m-%d')
        if changeTime < nowTime:
            error_message['change_date'] = '调课日期 change_date 不能是之前的日期'
        change_class = data.get('change_class', [])
        if not change_class:
            error_message['change_class'] = '调整后的课节 change_class 参数是必须的'
        if change_class and (len(original_class) != len(change_class)):
            error_message['change_class'] = '课节数不匹配'
        data['teacher_id'] = id
        # 调课
        if change_type == 0:
            data['change_teacher'] = id
        else:
            # 代课
            if not data.get('change_teacher'):
                error_message['change_teacher'] = '代课老师 change_teacher 不能为空'
            else:
                    data['change_teacher'] = data.get('change_teacher')
        if (error_message):
            return {'errors': error_message}

        return data

    def adjustClassSection(self, request):
        data = self.validate(request.data, request.user.id)  # 获取请求参数 对数据进行验证

        if data.get('errors'):
            return Response(data, status=400)
        '''
        4号 7放开
        赵： 1号-》4号  2，3---1，9
        1号 2 ---4号第7 
        formData: {
        original_date: '原课节日期',
        change_date: '改变日期',
        change_type: 0, 调课 1 代课
        change_teacher: '代课老师',
        original_class: [], 原课节--元素数字
        change_class: [], 调课节--元素数字
        course_plan:0 排课id
        },
        '''
        # 根据排课id 获取 本班的正课时间0.-
        try:
            cp = CoursePlan.objects.get(pk=data['course_plan'])
            classTime = cp.class_time.split(',')  # 列表中的元素是字符串
            # 验证接收到的 原课节 是不是正课
            for i in data['original_class']:
                if str(i) not in classTime:
                    return Response({'errors': '原课节只能是' + cp.class_time})
        except:
            return Response({'errors': 'course_plan 参数错误 找不到对应的排课信息'})
        # 获取代课讲师正常的正课时间
        print('change_teacher,change_teacher',data['change_teacher'])
        cp = self.getCp(data['change_teacher'])
        userClassTime = []
        if cp:
            for c in cp:
                userClassTime.extend(c.class_time.split(','))
        print("*"*50)
        print('用户正常的正课时间:',userClassTime)# 2 3 5 6

        # 获取代课讲师 change_date 这一天实际的正课时间
        print('userClassTime,userClassTime,userClassTimeuserClassTime',userClassTime)
        result = AdjustClassTime.objects.filter(teacher_id=data['change_teacher'], original_date=data['change_date'])

        for i in result:
            ajc = i.adjustclassmap_set.filter(is_take_effect=True)
            for a in ajc:
                if a.initial==a.final and i.original_date==i.change_date:
                    continue
                cl=a.initial.split('-')[-1]
                if cl in userClassTime:
                    userClassTime.remove(a.initial.split('-')[-1])
        print('用户实际的正课时间:', userClassTime)
        #获取代课讲师 调代课之后的 正课时间
        result = AdjustClassTime.objects.filter(change_teacher_id=data['change_teacher'],change_date=data['change_date'])
        classMap = {}
        for i in result:
            ajc = i.adjustclassmap_set.filter(is_take_effect=True)
            for a in ajc:
                classMap[a.initial] = a.final
        classMapList=list(map(lambda x:x.split('-')[-1],list(classMap.values())))
        print('用户调整后的正课时间:', classMapList)
        userClassTime.extend(classMapList)
        print('要改变的日期:', data['change_class'])
        print('用户当天的正课时间:', userClassTime)

        occupyClass=list(set(userClassTime) & set(list(map(str,data['change_class']))))
        if occupyClass:
            return Response({'errors': f"{data['change_date']}第{str(occupyClass)}节课已经被占用了~"})
        result=AdjustClassTime.objects.create(course_plan_id=data['course_plan'],original_date=data['original_date'],
                                              change_date=data['change_date'],change_type=data['change_type'],
                                              change_teacher_id=data['change_teacher'],teacher_id=data['teacher_id'])
        for index,item in enumerate(data['change_class']):
            initial=f'{result.original_date}-{data["original_class"][index]}'
            AdjustClassMap.objects.filter(act__teacher_id=data['teacher_id'],initial=initial).update(is_take_effect=False)
            AdjustClassMap.objects.create(act=result,final=f'{result.change_date}-{item}',initial=initial)
        return Response({})

    #获取用户当天的课节
    def getClassSection(self,request):
        coursePlan=self.getCp(request.user.id)
        #将课节 对应 排课对象
        userClassTime = {}
        if coursePlan:
            for i in coursePlan:
                no_class = i.teaching_time.no_class.split(',')
                am_class = i.teaching_time.am_class.split(',')
                pm_class = i.teaching_time.pm_class.split(',')
                for cs in i.class_time.split(','):
                    userClassTime[cs]=i
        else:
            return  Response('暂无数据')
        #判断不上课  上午上课  下午上课
        if timezone.now().strftime("%Y-%m-%d") in am_class:
            print('上午上课')
            userClassTimecopy = copy.deepcopy(userClassTime)
            for k in userClassTimecopy:
                if int(k) > 4:
                    del userClassTime[k]
        if timezone.now().strftime("%Y-%m-%d") in pm_class:
            print('下午上课')
            userClassTimecopy =copy.deepcopy(userClassTime)
            for k in userClassTimecopy:
                if int(k)<5:
                    del userClassTime[k]
        if timezone.now().strftime("%Y-%m-%d") in no_class:
            return Response({'data':'今天没有课'})
        print("*" * 50)
        print('用户正常的正课时间:', userClassTime)  # 2 3 5 6

        # 获取该讲师 当天调走的所有正课
        result = AdjustClassTime.objects.filter(teacher_id=request.user.id, original_date=timezone.now().strftime("%Y-%m-%d"),state=1)
        for i in result:
            ajc = i.adjustclassmap_set.filter(is_take_effect=True)
            for a in ajc:
                cs = a.initial.split('-')[-1] #课节
                if cs in userClassTime:
                    del userClassTime[cs]

        #             userClassTime.remove(a.initial.split('-')[-1])
        print('用户实际的正课时间:', userClassTime)
        # 班级 讲师 导员 课程（阶段）调代课状态 课程日期 原课节 课节 点名状态 点名时间
        classSection=[]
        for (cs,cp) in userClassTime.items():
            print(timezone.now().strftime("%Y-%m-%d"),cs,cp.room_number.number)
            print(123,RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=cs,room_number=cp.room_number.number))
            data={
                'id':RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=cs,room_number=cp.room_number.number).id,
                'department':cp.classid.college.name,
                'class_name':cp.classid.name,
                'lecturer':cp.lecturer.name,
                'counsellor':cp.counsellor.name,
                'course':f'{cp.course.name}({cp.course.stage})',
                'type':'',
                'date':timezone.now().strftime("%Y-%m-%d"),
                'original_cs':cs,
                'cs':cs,
                'state':RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=cs,room_number=cp.room_number.number).state,
                'rollcall_time':RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=cs,room_number=cp.room_number.number).update_time
            }
            classSection.append(data)

        # 获取该讲师 调代课之后的 正课时间
        result = AdjustClassTime.objects.filter(state=1,change_teacher_id=request.user.id,
                                                change_date=timezone.now().strftime("%Y-%m-%d"))
        for i in result:
            ajc = i.adjustclassmap_set.filter(is_take_effect=True)
            for a in ajc:
                #classMap[a.initial] = a.final
                type ='代课' if i.change_type else '调课'
                data = {
                    'id':RollCall.objects.get(class_date=i.original_date.strftime("%Y-%m-%d"),class_section=a.initial.split('-')[-1],room_number=i.course_plan.room_number.number).id,
                    'department': i.course_plan.classid.name,
                    'class_name': i.course_plan.classid.name,
                    'lecturer': i.teacher.name,
                    'counsellor': i.course_plan.counsellor.name,
                    'course': f'{i.course_plan.course.name}({i.course_plan.course.stage})',
                    'type':type,
                    'date': a.initial.rsplit('-',maxsplit=1)[0],
                    'original_cs': a.initial.split('-')[-1],
                    'cs': a.final.split('-')[-1],
                    'state': RollCall.objects.get(class_date=i.original_date.strftime("%Y-%m-%d"),class_section=a.initial.split('-')[-1],room_number=i.course_plan.room_number.number).state,
                    'rollcall_time': RollCall.objects.get(class_date=i.original_date.strftime("%Y-%m-%d"),class_section=a.initial.split('-')[-1],room_number=i.course_plan.room_number.number).update_time
                }
                classSection.append(data)
        return Response(classSection)

    # 获取当天所有班级的课节
    def getClassSectionall(self,request):
        coursePlan=CoursePlan.objects.all()
        for k in coursePlan:
            #将课节 对应 排课对象
            userClassTime = {}
            for i in coursePlan:
                no_class = i.teaching_time.no_class.split(',')
                am_class = i.teaching_time.am_class.split(',')
                pm_class = i.teaching_time.pm_class.split(',')
                for cs in i.class_time.split(','):
                    userClassTime[cs]=i
            #判断不上课  上午上课  下午上课
            if timezone.now().strftime("%Y-%m-%d") in am_class:
                print('上午上课')
                userClassTimecopy = copy.deepcopy(userClassTime)
                for k in userClassTimecopy:
                    if int(k) > 4:
                        del userClassTime[k]
            if timezone.now().strftime("%Y-%m-%d") in pm_class:
                print('下午上课')
                userClassTimecopy =copy.deepcopy(userClassTime)
                for k in userClassTimecopy:
                    if int(k)<5:
                        del userClassTime[k]
            if timezone.now().strftime("%Y-%m-%d") in no_class:
                return Response({'data':'今天没有课'})
            print("*" * 50)
            print('用户正常的正课时间:', userClassTime)  # 2 3 5 6

            # 获取该讲师 当天调走的所有正课
            result = AdjustClassTime.objects.filter(teacher_id=request.user.id, original_date=timezone.now().strftime("%Y-%m-%d"),state=1)
            for i in result:
                ajc = i.adjustclassmap_set.filter(is_take_effect=True)
                for a in ajc:
                    cs = a.initial.split('-')[-1] #课节
                    if cs in userClassTime:
                        del userClassTime[cs]

            #             userClassTime.remove(a.initial.split('-')[-1])
            # print('用户实际的正课时间:', userClassTime)
            # 班级 讲师 导员 课程（阶段）调代课状态 课程日期 原课节 课节 点名状态 点名时间
            classSection=[]
            for (cs,cp) in userClassTime.items():
                data={
                    'id':RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=cs,room_number=cp.room_number.number).id,
                    'department':cp.classid.college.name,
                    'class_name':cp.classid.name,
                    'lecturer':cp.lecturer.name,
                    'counsellor':cp.counsellor.name,
                    'course':f'{cp.course.name}({cp.course.stage})',
                    'type':'',
                    'date':timezone.now().strftime("%Y-%m-%d"),
                    'original_cs':cs,
                    'cs':cs,
                    'state':RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=cs,room_number=cp.room_number.number).state,
                    'rollcall_time':''
                }
                classSection.append(data)
            print(RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=cs,room_number=cp.room_number.number).state,'id')
            # 获取该讲师 调代课之后的 正课时间
            result = AdjustClassTime.objects.filter(state=1,change_teacher_id=request.user.id,
                                                    change_date=timezone.now().strftime("%Y-%m-%d"))
            for i in result:
                ajc = i.adjustclassmap_set.filter(is_take_effect=True)
                for a in ajc:
                    #classMap[a.initial] = a.final
                    type ='代课' if i.change_type else '调课'
                    print(RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=a.initial.split('-')[-1],room_number=i.course_plan.room_number.number))
                    data = {
                        'id':RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=a.initial.split('-')[-1],room_number=i.course_plan.room_number.number).id,
                        'department': i.course_plan.classid.name,
                        'class_name': i.course_plan.classid.name,
                        'lecturer': i.teacher.name,
                        'counsellor': i.course_plan.counsellor.name,
                        'course': f'{i.course_plan.course.name}({i.course_plan.course.stage})',
                        'type':type,
                        'date': a.initial.rsplit('-',maxsplit=1)[0],
                        'original_cs': a.initial.split('-')[-1],
                        'cs': a.final.split('-')[-1],
                        'state': RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=a.initial.split('-')[-1],room_number=i.course_plan.room_number.number).state,
                        'rollcall_time': ''
                    }
                    classSection.append(data)
            print(RollCall.objects.get(class_date=timezone.now().strftime("%Y-%m-%d"),class_section=a.initial.split('-')[-1],room_number=i.course_plan.room_number.number).state,'ids')
        return Response(classSection)

class AdjustClassTimes(ModelViewSet):
    queryset = AdjustClassTime.objects.all()
    serializer_class = AdjustClassTimeSerializers

    # 实现局部更新
    def update(self, request,pk, *args, **kwargs):
        id = self.kwargs.get('pk')
        if request.data['state'] == 2:
            # adjust = AdjustClassTime.objects.get(id=pk)
            # asd=AdjustClassMap.objects.filter(act=adjust)
            asd = AdjustClassMap.objects.filter(act_id=id)
            for i in asd:
                i.is_take_effect=False
                i.save()
        else:
            # 调课的课节映射记录
            acm = AdjustClassMap.objects.filter(act_id=id)
            for i in acm:
                # 获取调课记录的 原课节日期 和 原课节
                date, section = i.initial.rsplit('-', maxsplit=1)
                # 获取调课记录的 新课节日期 和 新课节
                actual_date, actual_section = i.final.rsplit('-', maxsplit=1)
                RollCall.objects.filter(teaching_time_id=i.act.course_plan.teaching_time_id, class_date=date,
                                        class_section=section, lecturer=i.act.teacher.name).update(
                    actual_date=actual_date, actual_section=actual_section, lecturer=i.act.change_teacher.name,
                    act_id=id,class_name=AdjustClassTime.objects.get(id=id).course_plan.classid.name)
        return super(AdjustClassTimes, self).update(request, partial=True)
        # return super().update(request, partial=True)

# #讲师的课表视图
# class RollCallView(CreateAPIView,GenericViewSet,ListModelMixin,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin):
#     serializer_class = RollCallSerializer
#     queryset = RollCall.objects.all()
#
#     def get_queryset(self):
#         # return RollCall.objects.filter(lecturer=self.request.user.name,class_date__lte=timezone.now()).order_by('-state','-actual_date','actual_section')
#         return RollCall.objects.filter(lecturer=self.request.user.name).order_by(
#             '-state', '-actual_date', 'actual_section')
#     def retrieve(self,request,*args,**kwargs):
#         instance = self.get_object()
#         data = {'state':0,'students':[]}
#         print(instance,'instance')
#         #查询班级的学生信息
#         if instance.state == 0:
#             # if(instance.)
#             classObj = Class_a.objects.get(name=instance.class_name,college_id=Department.objects.get(name = instance.department).id)
#             students = Student.objects.filter(cls=classObj).values('name','idcardnumber')
#             data['students'] = list(students)
#         else:
#             normal = instance.normal.split(',') if instance.normal else []
#             cut_classes = instance.cut_classes.split(',') if instance.cut_classes else []
#             leave = instance.leave.split(',') if instance.leave else []
#             late = instance.late.split(',') if instance.late else []
#             idcardnumber = normal+cut_classes+leave+late
#             students = Student.objects.filter(idcardnumber__in = idcardnumber).values('name','idcardnumber')
#             for s in students:
#                 #出勤:1   旷课:2    请假:3   迟到:4
#                 s['state'] = 1
#                 if s['idcardnumber'] in cut_classes:
#                     s['state'] = 2
#                 if s['idcardnumber'] in leave:
#                     s['state'] = 3
#                 if s['idcardnumber'] in late:
#                     s['state'] = 4
#                 data['students'].append(s)
#                 data['state'] = 1
#         return Response(data)
#
#     def update(self, request, *args, **kwargs):
#         return super(RollCallView, self).update(request, partial=True)

class GetasjustClas(APIView):
    def get(self,request):
        adjust = AdjustClassTime.objects.all()
        nopass = AdjustClassTime.objects.filter(state=2)
        list=[]
        list2=[]
        for i in nopass:
            dict = {}
            dict['id'] = i.id
            dict['department'] = i.course_plan.classid.college.name
            dict['stage'] = i.course_plan.classid.stage
            dict['name'] = i.course_plan.classid.name
            dict['teacher'] = i.teacher.name
            dict['counsellor'] = i.course_plan.counsellor.name
            dict['original_date'] = i.original_date
            dict['change_date'] = i.change_date
            initial = []
            final = []
            for k in i.adjustclassmap_set.all():
                initial.append(k.initial.rsplit('-')[-1])
                final.append(k.final.rsplit('-')[-1])
            dict['initial'] = initial
            dict['final'] = final
            dict['change_type'] = i.change_type
            dict['change_teacher'] = i.change_teacher.name
            dict['createtime'] = i.createtime.strftime("%Y-%m-%d %H:%M")
            dict['state'] = i.state
            if dict['initial'] == []:
                continue
            list2.append(dict)

        for i in adjust:
            dict={}
            dict['id']=i.id
            dict['department'] = i.course_plan.classid.college.name
            dict['stage'] = i.course_plan.classid.stage
            dict['name']=i.course_plan.classid.name
            dict['teacher'] = i.teacher.name
            dict['counsellor'] = i.course_plan.counsellor.name
            dict['original_date'] = i.original_date
            dict['change_date'] = i.change_date
            initial = []
            final = []
            for k in i.adjustclassmap_set.all():
                if(k.is_take_effect==True):
                    initial.append(k.initial.rsplit('-')[-1])
                    final.append(k.final.rsplit('-')[-1])
            dict['initial'] = initial
            dict['final'] = final
            dict['change_type'] = i.change_type
            dict['change_teacher'] = i.change_teacher.name
            dict['createtime'] = i.createtime.strftime("%Y-%m-%d %H:%M")
            dict['state']=i.state
            if dict['initial'] ==[]:
                continue
            list.append(dict)

        return Response({'content':list,'nocontent':list2})

#讲师的课表视图
class RollCallView(ModelViewSet):
    serializer_class = RollCallSerializer
    queryset = RollCall.objects.all()
    #根据教学周期id和学院id 获取每个讲师带了多少节课
    def getClassSections(self,request):
        # 获取当前的教学周期id
        tc = self.request.query_params.get('tc_id')
        #获取学院id
        college=self.request.query_params.get('college_id')
        # 根据教学周期id 获取已经点名课表
        result=RollCall.objects.filter(teaching_time_id=tc, state=True,college_id=college).values('lecturer_id').annotate(section_num=Count('id')).values('section_num','lecturer','college__name','teaching_time__title','lecturer_id','teaching_time_id')
        return Response(list(result))
    #获取某一个老师 带课程对应的的课节
    def getClassInfo(self,request):
        lecturer_id=self.request.query_params.get('lecturer_id')
        tc = self.request.query_params.get('tc_id')
        result = RollCall.objects.filter(teaching_time_id=tc, state=True, lecturer_id=lecturer_id).values(
            'class_id').annotate(section_num=Count('id')).values('section_num', 'lecturer','class_name','college__name','course')
        return Response(list(result))
    def retrieve(self, request, *args, **kwargs):
        instance=self.get_object()#获取单个课表对象
        data={'state':0,'students':[]}
        #查询班级的学生信息
        if instance.state == 0:
            #没有点名
            classObj=Class_a.objects.get(name=instance.class_name,college_id=instance.college_id)
            # classObj = Class_a.objects.get(name=instance.class_name)
            students=Student.objects.filter(cls=classObj).values('name','idcardnumber')
            data['students']=list(students)
        else:
            normal=instance.normal.split(',') if instance.normal else []
            cut_classes=instance.cut_classes.split(',') if instance.cut_classes else []
            leave=instance.leave.split(',') if instance.leave else []
            late=instance.late.split(',') if instance.late else []

            idcardnumber=normal+cut_classes+leave+late
            students=Student.objects.filter(idcardnumber__in=idcardnumber).values('name','idcardnumber')
            for s in students:
                #出勤：1 旷课：2 请假：3 迟到：4
                s['state'] = 1 # 学生的出勤状态
                if s['idcardnumber'] in cut_classes:
                    s['state']=2
                if s['idcardnumber'] in leave:
                    s['state']=3
                if s['idcardnumber'] in late:
                    s['state']=4
                data['students'].append(s)
                data['state']=1#该课表是否已经被点名
        return Response(data)
    def update(self, request, *args, **kwargs):
        return super(RollCallView, self).update(request,partial=True)
    #根据讲师 获取讲师的点名表
    def getPointNameTable(self,request):
        self.queryset=RollCall.objects.filter(lecturer=self.request.user.name, class_date__lte=timezone.now()).order_by('state','-actual_date','actual_section')
        return self.list(request)
    #获取出勤率的方法
    def getAttendance(self,request):
        page=request.query_params.get('page',1)
        page_size=request.query_params.get('page_size',5)
        if page_size>20:
            page_size=20
        show_type = request.query_params.get('show_type')  # 展示类型
        date=request.query_params.get('date',timezone.now().strftime('%Y-%m-%d'))#日期
        start=request.query_params.get('start')#开始时间
        end=request.query_params.get('end')#结束时间
        tc_id=request.query_params.get('tc_id')#教学周期
        type=request.query_params.get('type')# 类型：学院、班级、阶段
        type_field={'class':'class_id','stage':'college_stage_id','college':'college_id'}
        group_field=type_field.get(type,'class_id')
        college_id = request.query_params.get('college_id')

        where=Q(state=True)
        if college_id:
            where.add(Q(college_id=college_id),Q.AND)
        #判断展示类型
        if show_type=='1':
            where.add(Q(actual_date=date),Q.AND)
        elif show_type=='2':
            where.add(Q(actual_date__range=(start,end)),Q.AND)
        elif show_type=='3':
            where.add(Q(teaching_time_id=tc_id),Q.AND)

        queryset = RollCall.objects.filter(where).values(group_field).annotate(
            total_studends_num=Sum('students_num'), total_attendance_num=Sum('attendance_num'))

        # queryset = RollCall.objects.filter(where).values('college_id').annotate(total_studends_num=Sum('students_num'),total_attendance_num=Sum('attendance_num')).values('class_name', 'total_studends_num', 'total_attendance_num','college__name')
        # print(queryset)
        # return  Response({})


        if group_field=='class_id':
            result=queryset.values('class_name', 'total_studends_num', 'total_attendance_num','teaching_time__title','college__name')
        elif group_field=='college_stage_id':
            result=queryset.values('college_stage__name','college__name','teaching_time__title', 'total_studends_num', 'total_attendance_num')
        else:
            result = queryset.values('college__name', 'teaching_time__title','total_studends_num', 'total_attendance_num')
        start=(page-1)*page_size
        data={'count':result.count(),'data':list(result[start:page*page_size])}
        return Response(data)

