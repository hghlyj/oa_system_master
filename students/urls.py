from rest_framework import routers
from django.urls import path
from students.views import ClassView, StudentView
from students import views
urlpatterns=[
    path('download_excel_temp',views.download_excel_temp),
    path('students/roll-call',StudentView.as_view({
        'get':'getStudentsRollCall'
    }))
]

router=routers.DefaultRouter(trailing_slash=False)#取消url地址后面的 /
router.register('classes',ClassView,basename='class')
router.register('students',StudentView,basename='students')
urlpatterns+=router.urls