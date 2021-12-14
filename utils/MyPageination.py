from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
# 分页器
class MyPageination(PageNumberPagination):
    # 默认情况下每页显示五条数据
    page_size = 5
    # 接收每页显示条数的 参数
    page_size_query_param = 'page_size'
    # 每页最大显示条数
    max_page_size = 6
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            # 总条数
            ('count', self.page.paginator.count),
            ('page_count',self.page.paginator.num_pages),
            ('results', data)
        ]))