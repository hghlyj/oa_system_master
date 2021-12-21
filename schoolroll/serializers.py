from rest_framework import serializers
from .models import *
class SchoolrollSerializers(serializers.ModelSerializer):
    # name = serializers.CharField(label='部门',max_length=10,validators=[UniqueValidator(queryset=Department.objects.all(),message='该部门已存在，无需重复添加')])
    class Meta:
        model = Schoolroll
        fields = '__all__'



