from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


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