from django.urls import path
from rest_framework import routers
from .views import Schoolrolls
from . import views

urlpatterns = [

]

router=routers.DefaultRouter(trailing_slash=False)#取消url地址后面的 /
router.register('schoolroll',Schoolrolls,basename='adminuser')

urlpatterns+=router.urls
