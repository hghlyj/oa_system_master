from rest_framework import serializers
from django.db import models
import datetime
import json

from register.models import Department
from .models import TeachingTime, CoursePlan, Classroom, Courses, AdjustClassTime, RollCall, CollegeStage


class TeachingTimeSerializers(serializers.ModelSerializer):
    class Meta:
        model =TeachingTime
        fields= '__all__'

class CoursePlanSerializers(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     coursePlan=super(CoursePlanSerializers, self).create(validated_data)
    #     print(validated_data,123456)
    #     RollCall(teaching_time=validated_data['teaching_time'].id, department=validated_data['room_number'].department,room_number=validated_data['room_number'].number,
    #                               college=validated_data['lecturer'].name,lecturer=validated_data['lecturer'].name, counsellor=validated_data['counsellor'].name,
    #                               course=f"{validated_data['course'].name}({validated_data['course'].stage})",
    #                               class_name=validated_data['classid'].name,class_date=datestart,class_section=s,actual_date=datestart,actual_section=s)
    #     return coursePlan

    def create(self, validated_data):
        coursePlan=super(CoursePlanSerializers, self).create(validated_data)
        # #生成课表
        print(validated_data,456789)
        teachingTime=validated_data['teaching_time']#教学周期对象
        start=teachingTime.starttime.strftime('%Y-%m-%d')
        end=teachingTime.endtime.strftime('%Y-%m-%d')
        datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
        morning=teachingTime.am_class.split(',')
        afternoon=teachingTime.pm_class.split(',')
        noclass=teachingTime.no_class.split(',')
        rcList=[]
        while datestart <= dateend:
            cs = validated_data['class_time'].split(',')
            #判断是上午上课还是下午上课
            if datestart.strftime('%Y-%m-%d') in morning:
                cs=cs[0:2]
            if datestart.strftime('%Y-%m-%d') in afternoon:
                cs=cs[2:4]
            if datestart.strftime('%Y-%m-%d') in noclass:
                cs=[]
            for s in cs:
                print(validated_data,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',type(validated_data['teaching_time'].id))
                rc = RollCall(teaching_time=validated_data['teaching_time'],
                            lecturer_id= validated_data['lecturer'].id,
                            class_id= validated_data['classid'].id,
                            # act
                            college=validated_data['room_number'].department,
                            course_plan=CoursePlan.objects.get(teaching_time_id=validated_data['teaching_time'].id),
                            department=validated_data['room_number'].department,
                            lecturer = validated_data['lecturer'].name,
                            counsellor=validated_data['counsellor'].name,
                            class_name = validated_data['classid'].name,
                            room_number=validated_data['room_number'].number,
                            class_date = datestart,
                            class_section = s,
                            actual_section = s,
                            actual_date = datestart,
                            course = f"{validated_data['course'].name}({validated_data['course'].stage})",
                           )
                print(rc.__dict__)
                rcList.append(rc)

            datestart += datetime.timedelta(days=1)
        RollCall.objects.bulk_create(rcList)
        return  coursePlan

    # def update(self, validated_data):
    #     coursePlan=super(CoursePlanSerializers, self).update(validated_data)
    #     # #生成课表
    #     teachingTime=validated_data['teaching_time']#教学周期对象
    #     start=teachingTime.starttime.strftime('%Y-%m-%d')
    #     end=teachingTime.endtime.strftime('%Y-%m-%d')
    #     datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    #     dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    #     morning=teachingTime.am_class.split(',')
    #     afternoon=teachingTime.pm_class.split(',')
    #     noclass=teachingTime.no_class.split(',')
    #     while datestart <= dateend:
    #         cs = validated_data['class_time'].split(',')
    #         #判断是上午上课还是下午上课
    #         if datestart.strftime('%Y-%m-%d') in morning:
    #             cs=cs[0:2]
    #         if datestart.strftime('%Y-%m-%d') in afternoon:
    #             cs=cs[2:4]
    #         if datestart.strftime('%Y-%m-%d') in noclass:
    #             cs=[]
    #         for s in cs:
    #             RollCall.objects.get(teaching_time)
    #             rc = RollCall.objects.get(teaching_time=validated_data['teaching_time'], department=validated_data['room_number'].department,room_number=validated_data['room_number'].number,
    #                           lecturer=validated_data['lecturer'].name, counsellor=validated_data['counsellor'].name,
    #                           course=f"{validated_data['course'].name}({validated_data['course'].stage})",
    #                           class_name=validated_data['classid'].name,class_date=datestart,class_section=s,actual_date=datestart,actual_section=s)
    #         datestart += datetime.timedelta(days=1)
    #     return  coursePlan

    class Meta:
        model =CoursePlan
        fields= '__all__'


class ClassroomSerializers(serializers.ModelSerializer):
    department=serializers.SlugRelatedField(slug_field='name',queryset=Department.objects.all())
    class Meta:
        model =Classroom
        fields= '__all__'

class CoursesSerializers(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    school_id = serializers.IntegerField(write_only=True)
    college_stage = serializers.StringRelatedField()
    college_stage_id = serializers.IntegerField(write_only=True)
    class Meta:
        model =Courses
        fields= '__all__'


class AdjustClassTimeSerializers(serializers.ModelSerializer):
    class Meta:
        model =AdjustClassTime
        fields= '__all__'

class UserCoursePlanSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    lecturer = serializers.StringRelatedField(read_only=True)
    counsellor = serializers.StringRelatedField(read_only=True)
    room_number = serializers.CharField(max_length=30)
    class_time = models.CharField(max_length=20)
    course =CoursesSerializers()
    cls = serializers.StringRelatedField(read_only=True)
    cls_id=serializers.IntegerField()
    class Meta:
        model=CoursePlan
        fields='__all__'

#课表序列化器
class RollCallSerializer(serializers.ModelSerializer):
    class Meta:
        model=RollCall
        fields='__all__'

# 学院课程阶段
class CollegeStageSerializer(serializers.ModelSerializer):
    college_id=serializers.IntegerField(write_only=True)
    college=serializers.StringRelatedField()
    class Meta:
        model = CollegeStage
        fields = '__all__'