from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import PutIntoEffect,AwardedMarks,SubtractMarks,Disciplinetype,StudentScore
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet
from rest_framework.viewsets import ModelViewSet, GenericViewSet
import django_filters
from collections import OrderedDict
from django_filters import rest_framework as filters
from .serializers import AwardedMarksSerializer,SubtractMarksSerializer,DisciplinetypeSerializer,SubtractMarksSerializerw,MarksListSerializer

class CustomPagination(PageNumberPagination):
	page_size = 5 #每页显示的条数
	max_page_size = 100 #每页最多显示的记录数
	#考虑如何接收一个 每页显示条数的参数 参数名？
	page_size_query_param = 'page_size'
	def get_paginated_response(self, data):
		return Response(OrderedDict([
			('count', self.page.paginator.count),#数据记录总条数
			('current_page', self.page.number),#当前的页码
			('total_page', self.page.paginator.num_pages),#总页数
			('data', data)#当前页展示的数据

		]))
def xTree(datas):
	lists = []
	tree = {}
	for i in datas:
		item = i
		tree[item['id']] = item
	for i in datas:

		obj = i
		if not obj['pid']:
			root = tree[obj['id']]
			lists.append(root)
		else:
			parent_id = obj['pid']
			if 'childlist' not in tree[parent_id]:
				tree[parent_id]['childlist'] = []
			tree[parent_id]['childlist'].append(tree[obj['id']])
	return lists

class PutIntoEffects(APIView):
	def get(self,request):
		id=request.GET.get('id')
		list = PutIntoEffect.objects.filter(putintoeffect_id=id).values()
		list2=[]
		for i in list:
			list2.append(i)
		list3 = xTree(list2)
		return Response({'list':list3,'code':200})


class AwardedMarkssFilter(FilterSet):
	content = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = AwardedMarks
		fields = ['content']


class AwardedMarkss(ModelViewSet):
	queryset = AwardedMarks.objects.all()  # 查询集
	serializer_class = AwardedMarksSerializer  # 序列化器

	pagination_class  = CustomPagination #分页
	filter_backends = (filters.DjangoFilterBackend,)
	filterset_class = AwardedMarkssFilter

	# @action(methods=['get'], detail=False)
	# def children(self,request):
	# 	list =  AwardedMarks.objects.all().values()
	# 	list1=[]
	# 	for i in list:
	# 		list1.append(i)
	# 	# list2 = xTree(list1)
	# 	return Response({'list': list1, 'code': 200})

	def list(self, request, *args, **kwargs):
		no = request.query_params.get('no')
		if (no == '1'):
			self.pagination_class = None  # 不分页
		print(111111111111,self.pagination_class)
		return super(AwardedMarkss,self).list(request)

	def update(self, request, *args, **kwargs):
		return super(AwardedMarkss, self).update(request, partial=True)

class Disciplinetypes(ModelViewSet):
	queryset = Disciplinetype.objects.all()  # 查询集
	serializer_class = DisciplinetypeSerializer  # 序列化器

	def list(self, request, *args, **kwargs):
		self.pagination_class = None  # 不分页
		return super(Disciplinetypes,self).list(request)


class SubtractMarkssFilter(FilterSet):
	content = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = SubtractMarks
		fields = ['Disciplinetype','content']


class SubtractMarkss(ModelViewSet):
	queryset = SubtractMarks.objects.all()  # 查询集
	serializer_class = SubtractMarksSerializer  # 序列化器
	filter_backends = (filters.DjangoFilterBackend,)
	filterset_class = SubtractMarkssFilter


	def list(self, request, *args, **kwargs):
		no = request.query_params.get('no')
		if (no == '1'):
			self.pagination_class = None  # 不分页
		return super(SubtractMarkss,self).list(request)

class SubtractMarkssw(ModelViewSet):
	queryset = SubtractMarks.objects.all()  # 查询集
	serializer_class = SubtractMarksSerializerw  # 序列化器


class MarksListsFilter(FilterSet):
	class Meta:
		model = StudentScore
		fields = ['state','name','depar','cls','lecturer','counsellor','market','status']
class StudentScores(ModelViewSet):
	queryset = StudentScore.objects.all()  # 查询集
	serializer_class = MarksListSerializer  # 序列化器
	filter_backends = (filters.DjangoFilterBackend,)
	filterset_class = MarksListsFilter

	# 实现局部更新
	def update(self, request, *args, **kwargs):
		return super(StudentScore,self).update(request, partial=True)



class BookInfoViewSet(GenericViewSet):
	# 保存图片
	@action(methods=['post'], detail=False)
	def save_image(self, request):
		file = request.FILES.get('file')
		print(file.name)
		try:
			# 构造图片保存路径
			file_path = 'static/ScoreMarksImg/' + file.name
			# 保存图片
			with open(file_path, 'wb+') as f:
				f.write(file.read())
				f.close()
			response = {'file': file.name, 'code': 200, 'msg': "添加成功"}
		except:
			response = {'file': '', 'code': 201, 'msg': "添加失败"}
		return Response(response)


