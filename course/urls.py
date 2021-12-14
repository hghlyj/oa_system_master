from django.urls import path
from rest_framework import routers
from .views import *

urlpatterns = [
    path('usercourseplans',UserCoursePlanView.as_view({'put': 'adjustClassSection'})),
    path('getasjustClas',GetasjustClas.as_view()),
    path('class-sections', UserCoursePlanView.as_view({'get': 'getClassSection'})),
    path('class-sectionsall', UserCoursePlanView.as_view({'get': 'getClassSectionall'})),

    #获取讲师的课表（点名表）
    path('point_name_tables',RollCallView.as_view({'get':'getPointNameTable'})),
    #根据教学周期计算讲师课时
    path('class_sections',RollCallView.as_view({'get':'getClassSections'})),
    #获取某一位老师的课时
    path('user_class_sections',RollCallView.as_view({'get':'getClassInfo'})),
    #获取不同类型的教学周期 全部的 有效的 生效的
    path('teaching_cycles',TeachingTimes.as_view({'get':'getTeachingTime'})),
    path('class_attendances',RollCallView.as_view({'get':'getAttendance'}))
]

router=routers.DefaultRouter(trailing_slash=False)#取消url地址后面的 /
router.register('teachingtime',TeachingTimes,basename='teachingtime')
router.register('coursepian',CoursePlans,basename='coursepian')
router.register('classroom',Classrooms,basename='classroom')
router.register('courses',Coursess,basename='Courses')
router.register('adjustclasstime',AdjustClassTimes,basename='adjustclasstime')

#获取讲师的课表
router.register('class_timetables',RollCallView , basename='classtimetables')
#学院阶段
router.register('college_stages',CollegeStageView,basename='college_stages')
#获取讲师的课表
#router.register('class_timetables',RollCallView , basename='classtimetables')
urlpatterns+=router.urls
