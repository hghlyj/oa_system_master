from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import *
class DepartmentSerializers(serializers.ModelSerializer):
    name = serializers.CharField(label='部门',max_length=10,validators=[UniqueValidator(queryset=Department.objects.all(),message='该部门已存在，无需重复添加')])
    class Meta:
        model = Department
        fields = '__all__'

class RoleSerializers(serializers.ModelSerializer):
    department=serializers.SlugRelatedField(slug_field='name',queryset=Department.objects.all())
    # department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Role
        fields= '__all__'
        validators = [UniqueTogetherValidator(queryset=Role.objects.all(), fields=('role_name', 'department'),
                                              message='该职位已存在，无需重复添加！')]
class RoleSerializerss(serializers.ModelSerializer):
    department=serializers.SlugRelatedField(slug_field='label',queryset=Department.objects.all())
    # department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Role
        fields= '__all__'
        validators = [UniqueTogetherValidator(queryset=Role.objects.all(), fields=('role_name', 'department'),
                                              message='该职位已存在，无需重复添加！')]

class AdminUserSerializerss(serializers.ModelSerializer):
    Role=RoleSerializerss(many=True,read_only=True)

    class Meta:
        model = AdminUser
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff']
        read_only_fields = ['last_login', 'date_joined']
        # 给字段额外添加属性
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': True, 'allow_blank': False, 'trim_whitespace': True},
                        'last_name': {'required': True, 'allow_blank': False, 'trim_whitespace': True}}

class AdminUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        #fields = '__all__'
        exclude=['groups','user_permissions','is_superuser','is_staff']
        read_only_fields = ['last_login','date_joined']
        #给字段额外添加属性
        extra_kwargs = {'password': {'write_only': True},
                        'first_name':{'required':True,'allow_blank':False,'trim_whitespace':True},
                        'last_name':{'required':True,'allow_blank':False,'trim_whitespace':True}}

    def create(self, validated_data):
        user=super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

