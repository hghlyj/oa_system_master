from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from utils.ResponseJWTToken import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('register.urls')),
    path('api/', include('students.urls')),
    path('api/', include('course.urls')),
    path('api/', include('studentScore.urls')),
    path('api/', include('schoolroll.urls')),
    path('api/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
