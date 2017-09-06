import json
from django.db.models import Q
from base import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict
from .base import BaseServiceList
class Server(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'hostname', 'text': '主机名', 'condition_type': 'input'},
            {'name': 'ext_ip', 'text': '内部iP', 'condition_type': 'input'},
            {'name': 'int_ip', 'text': '外部iP', 'condition_type': 'input'},
        ]

        table_config = [
            {
                'q': 'id',
                'title': 'id',
                'display': 0,
                'text': {},
                'attr': {}
            },
            {
                'q': 'hostname',
                'title': '主机名',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@hostname'}},
                'attr': {'orginal': '@hostname', 'k2': 'v2'}
            },
            # '{n}-{m}'.format({'n': 'hostname','m':'@hostname'}) => hostname-c1.com
            {
                'q': 'ext_ip',
                'title': '外部IP',
                'display': 1,
                #    'text':{},
                #     'attr':{}
                'text': {'content': '{m}', 'kwargs': {'m': '@ext_ip'}},
                'attr': {'k1': '@port', 'k2': 'v2'}
            },
            {
                'q': 'int_ip',
                'title': '内部ip',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@int_ip'}},
                'attr': {'k1': '@business_unit_id', 'k2': 'v2'}
            },
        ]
        extra_select ={}
        super(Server, self).__init__(condition_config, table_config, extra_select)

    @property
    def device_status_list(self):

        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Base.status_choices)
        print(result)
        return list(result)

    @staticmethod
    def Server_condition(request):

            con_str = request.GET.get('condition', None)

            if not con_str:
                con_dict = {}
            else:
                con_dict = json.loads(con_str)

            con_q = Q()
            for k, v in con_dict.items():
                temp = Q()
                temp.connector = 'OR'
                for item in v:
                    temp.children.append((k, item))
                con_q.add(temp, 'AND')

            return con_q

    def fetch_services(self,request):
        response = BaseResponse()
        try:
            ret = {}

            conditions = self.Server_condition(request)

            asset_count = models.Base.objects.filter(conditions).count()
            print(asset_count,'count')
            page_info = PageInfo(request.GET.get('pager',None),asset_count)
            asset_list = models.Base.objects.filter(conditions).extra(select=self.extra_select).values(\
                *self.values_list)[page_info.start:page_info.end]
            ret['table_config'] = self.table_config
            print(5)
            ret['condition_config'] = self.condition_config
            print(3)
            ret['data_list'] = list(asset_list)
            print(1)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            print(2)
            ret['global_dict'] = {
                'device_status_list':self.device_status_list
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response


