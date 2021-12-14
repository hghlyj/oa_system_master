
from rest_framework import serializers


from register.models import AdminUser,Department
from students.models import Class_a, Student

class ClassSerializer(serializers.ModelSerializer):
    college=serializers.SlugRelatedField(queryset=Department.objects.all(),slug_field="name")
    number = serializers.CharField(read_only=True)
    room_number= serializers.CharField(read_only=True)
    teaching_time= serializers.CharField(read_only=True)
    class_time = serializers.CharField(read_only=True)
    course_plan= serializers.CharField(read_only=True)
    teacher= serializers.CharField(read_only=True)
    class Meta:
        model=Class_a
        fields='__all__'
class ClassSerializerw(serializers.ModelSerializer):
    class Meta:
        model=Class_a
        fields='__all__'


class StudentSerializerw(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'

class StudentSerializer(serializers.ModelSerializer):
    cls=serializers.SlugRelatedField(queryset=Class_a.objects.all(),slug_field="name")
    # department
    # cls = serializers.PrimaryKeyRelatedField(queryset=Class_a.objects.all(),many=True)
    # cls_set = ClassSerializer(many=True,read_only=True)  #反向查询获取所有数据
    # cls = serializers.StringRelatedField(many=True)
    class Meta:
        model=Student
        fields='__all__'



