from django.urls import path
from rest_framework import routers
from .views import AdminUsers, DepartmentView, RoleView
from . import views

urlpatterns = [

]

router=routers.DefaultRouter(trailing_slash=False)#取消url地址后面的 /
router.register('adminusers',AdminUsers,basename='adminuser')
router.register('departments',DepartmentView,basename='departments')
router.register('roles',RoleView,basename='roles')
urlpatterns+=router.urls
