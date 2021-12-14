from rest_framework import routers
from django.urls import path
from .views import PutIntoEffects,AwardedMarkss,SubtractMarkss,Disciplinetypes,SubtractMarkssw,StudentScores,BookInfoViewSet
urlpatterns=[
path('putintoeffect',PutIntoEffects.as_view()),
path('saveimage/', BookInfoViewSet.as_view({'post': 'save_image'})),#图片
]

router=routers.DefaultRouter(trailing_slash=False)#取消url地址后面的 /
router.register('awardedmarkss',AwardedMarkss,basename='awardedmarkss')
router.register('subtractmarkss',SubtractMarkss,basename='subtractmarkss')
router.register('subtractmarkssw',SubtractMarkssw,basename='subtractmarkssw')
router.register('disciplinetypes',Disciplinetypes,basename='disciplinetypes')
router.register('StudentScores',StudentScores,basename='disciplinetypes')
urlpatterns+=router.urls