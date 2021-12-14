import jwt
import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class Login(ModelViewSet):
    # queryset = AdminUser.objects.all()
    # serializer_class = AdminUserSerializers

    @action(methods=['post'], detail=False)
    def login(self, request):
        user = authenticate(request, **request.data)
        if user is not None:
            # 构造header
            headers = {
                'typ': 'jwt',
                'alg': 'HS256'
            }
            # 构造payload
            payload = {
                'user_id': user.id,  # 自定义用户ID
                'username': user.username,  # 自定义用户名
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)  # 超时时间
            }
            result = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256", headers=headers)
            return Response({'username': user.username, 'token': result})
        else:
            return Response({'error': '用户名或密码错误'})

    @action(methods=['post'], detail=False)
    def enroll(self,request):
        return self.create(request)