import json
import copy
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from datetime import datetime,timedelta
from .models import AdminUser, Department, Role
from course.models import CoursePlan, AdjustClassMap
from .serializers import AdminUserSerializers, DepartmentSerializers, RoleSerializers,AdminUserSerializerss

class AdminUsers(ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializers

    # 实现局部更新
    def update(self,request,*args,**kwargs):
        return super().update(request,partial=True)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=AdminUserSerializerss
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False)
    def deleteadminrole(self, request):
        depar_id = request.query_params.get('depar_id')
        role_id = request.query_params.get('role_id')
        return Response({'msg': '如何多对多删除一天数据'})

    #根据登录id获取该讲师带的班级信息
    #########################################################       还未考虑带两个班级情况
    #########################             不是本班班级无权进行调课
    @action(methods=['get'], detail=False)
    def adjuclass(self,requset):
        cls = CoursePlan.objects.filter(lecturer_id=requset.user.id)
        list = []
        for i in cls:
            list2=[]
            #原正课时间
            class_time = i.class_time.split(',')
            #本人调课     调走的不上    后来的上    带两个班级     需要根据排课进行判断
            #三个开关
            flag_me=False
            flag_change_me=False
            flag_me_change=False
            try:
                adjust_me= AdjustClassMap.objects.filter(act__teacher_id=requset.user.id,is_take_effect=True,act__change_type=0)
                flag_me=True
            except:
                print('a')
            #别人带给我的      代给我的是正课     //别人给我我就    还未拿到
            try:
                adjust_change_me = AdjustClassMap.objects.filter(is_take_effect=True,act__change_teacher_id=requset.user.id,act__change_type=1)
                flag_change_me=True
            except:
                print('b')
            #我把课代给别人    我的正课不上了
            try:
                adjust_me_change = AdjustClassMap.objects.filter(is_take_effect=True,act__teacher_id=requset.user.id,act__change_type=1)
                flag_me_change=True
            except:
                print('c')

            # 如果是时间格式，则转成字符串
            starttime = i.teaching_time.starttime.strftime('%Y-%m-%d')
            endtime = i.teaching_time.endtime.strftime('%Y-%m-%d')
            starttime = datetime.strptime(starttime, '%Y-%m-%d')
            endtime = datetime.strptime(endtime, '%Y-%m-%d')
            no_class = i.teaching_time.no_class.strip('"').split(',')
            am_class = i.teaching_time.am_class.strip('"').split(',')
            pm_class = i.teaching_time.pm_class.strip('"').split(',')
            while endtime>=starttime:
                dict={}
                classcopy = copy.deepcopy(class_time)
                time = starttime.strftime('%Y-%m-%d')
                if flag_me:
                    for k in adjust_me:
                        if  time==k.initial.rsplit("-", 1)[0]:
                            classcopy.remove(k.initial.rsplit("-", 1)[1])
                        if time == k.final.rsplit("-", 1)[0]:
                            classcopy.append(k.final.rsplit("-", 1)[1])
                            classcopy.sort()
                if flag_change_me:
                    for k1 in adjust_change_me:
                        if time == k1.final.rsplit("-", 1)[0]:
                            classcopy.append(k1.final.rsplit("-", 1)[1])
                            classcopy.sort()
                if flag_me_change:
                    for k2 in adjust_me_change:
                        if  time==k2.initial.rsplit("-", 1)[0]:
                            classcopy.remove(k2.initial.rsplit("-", 1)[1])
                dict['data']=time
                if(time not in no_class):
                    for w in classcopy:
                        if(dict['data'] in am_class):
                            if w in ['5','6','7','8']:
                                continue
                        if (dict['data'] in pm_class):
                            if w in ['1', '2', '3', '4']:
                                continue
                        if w == '1':
                            dict['one'] = True
                        if w == '2':
                            dict['two'] = True
                        if w == '3':
                            dict['three'] = True
                        if w == '4':
                            dict['four'] = True
                        if w == '5':
                            dict['five'] = True
                        if w == '6':
                            dict['six'] = True
                        if w == '7':
                            dict['seven'] = True
                        if w == '8':
                            dict['eight'] = True
                        if w == '9':
                            dict['nine'] = True
                        if w == '10':
                           dict['ten'] = True
                        if w == '11':
                            dict['eleven'] = True
                list2.append(dict)
                starttime=starttime+timedelta(days=1)
            list.append(list2)

        return Response({'msg':list})

    @action(methods=['get'], detail=False)
    def filter_js(self, request):
        part = request.query_params.get('part')
        content=[]
        for i in AdminUser.objects.all():   #循环教职工    获取一条
            for k in i.Role.all():   #循环职位
                a=k.department.name
                if(a==part):
                    if k.duty == '教学':      #获取职位为讲师的
                        obj={}
                        obj['id']=i.id
                        obj['name'] = i.name
                        if content ==[]:
                            content.append(obj)
                        else:
                            ids=[]
                            for w in content:
                                ids.append(w['id'])
                            if obj['id'] not in ids:
                                content.append(obj)
        return Response(content)
        # ser = self.get_serializer(list, many=True)
        # return Response(ser.data)


    @action(methods=['get'], detail=False)
    def filter_fdy(self, request):
        part = request.query_params.get('part')
        content = []
        for i in AdminUser.objects.all():
            for k in i.Role.all():
                a = k.department.name
                if (a == part):
                    if k.duty == '学管':
                        obj = {}
                        obj['id'] = i.id
                        obj['name'] = i.name
                        if content == []:
                            content.append(obj)
                        else:
                            ids = []
                            for w in content:
                                ids.append(w['id'])
                            if obj['id'] not in ids:
                                content.append(obj)
        return Response(content)
        # ser = self.get_serializer(list, many=True)
        # return Response(ser.data)


class DepartmentView(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers

    @action(methods=['get'],detail=False)
    def all(self,request):
        ser=self.get_serializer(self.get_queryset(),many=True)
        return Response(ser.data)

    @action(methods=['get'], detail=False)
    def allcoll(self, request):
        queryset = Department.objects.filter(label=1)
        ser = self.get_serializer(queryset, many=True)
        return Response(ser.data)


    # 修改教职工
    @action(methods=['get'], detail=False)
    def filter_depa(self,request):
        ids= request.query_params.get('ids')
        if ids:
            list=Role.objects.all().values()
            list2=[]
            list3=[]
            for i in list:
                list2.append(i)
            for k in list2:
                for w in json.loads(ids):
                    if k['id']==w:
                        list3.append(k)
            department_id=[]
            for s in list3:
                department_id.append(s['department_id'])

            queryset  = Department.objects.filter(id__in=department_id)
        ser = self.get_serializer(queryset,many=True)
        return Response(ser.data)

class RoleView(ModelViewSet):
    #角色表的查询
    def get_queryset(self):
        id = self.request.query_params.get('id')
        if id:
            return Role.objects.filter(department_id=id)
        return super().get_queryset()


    @action(methods=['get'], detail=False)
    def filter_roles(self,request):
        ids= request.query_params.get('ids')
        if ids:
            queryset  = Role.objects.filter(department_id__in=json.loads(ids))
        role_ids=request.query_params.get('role_ids')
        if role_ids:
            queryset = Role.objects.filter(id__in=json.loads(role_ids))
        ser = self.get_serializer(queryset,many=True)
        return Response(ser.data)

    queryset = Role.objects.all()
    serializer_class = RoleSerializers









