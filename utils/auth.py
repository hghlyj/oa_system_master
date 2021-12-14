from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from jwt import exceptions

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        try:
            verified_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'error': 'token已失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'error': '非法的token'})
        return (verified_payload,token)
