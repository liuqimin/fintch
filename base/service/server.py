import json
from base import models
from utils.pager import PageInfo
from django.db.models import Q
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
                'attr': {'name':'hostname','id':'@hotname','origin': '@hostname', 'edit-enable': 'true','edit-type': 'input'}
            },
            # '{n}-{m}'.format({'n': 'hostname','m':'@hostname'}) => hostname-c1.com
            {
                'q': 'ext_ip',
                'title': '外部IP',
                'display': 1,
                #    'text':{},
                #     'attr':{}
                'text': {'content': '{m}', 'kwargs': {'m': '@ext_ip'}},
                'attr': {'name':'ext_ip','id':'@ext_ip','origin': '@ext_ip', 'edit-enable': 'true','edit-type': 'input'}
            },
            {
                'q': 'int_ip',
                'title': '内部ip',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@int_ip'}},
                'attr': {'name':'int_ip','id':'@int_ip','origin': '@int_ip', 'edit-enable': 'true','edit-type': 'input'}
            },
            {
                'q': 'status',
                'title': '状态',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@@device_status_list'}},
                'attr': {'name':'status','id':'@status','orginal': '@status', 'edit-enable': 'true', 'edit-type': 'select',
                         'global-name': 'device_status_list'}
            },
        ]
        extra_select ={}
        super(Server, self).__init__(condition_config, table_config, extra_select)

    @property
    def device_status_list(self):

        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Base.status_choices)

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
            print(asset_count,'count',request.GET.get('pager')  )
            page_info = PageInfo(request.GET.get('pager',None),asset_count)
            asset_list = models.Base.objects.filter(conditions).extra(select=self.extra_select).values(\
                *self.values_list)[page_info.start:page_info.end]
            ret['table_config'] = self.table_config

            ret['condition_config'] = self.condition_config

            ret['data_list'] = list(asset_list)

            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }

            ret['global_dict'] = {
                'device_status_list':self.device_status_list
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_assets(request):
        response = BaseResponse()
        print('delete')
        try:
            delete_dict = QueryDict(request.body,encoding='utf-8')  ##get id_list
            id_list = delete_dict.getlist('id_list')
            models.Base.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        response = BaseResponse()
        print('save')
        try:
            put_dict = QueryDict(request.body,encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:

                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                    models.Base.objects.filter(id=nid).update(**row_dict)
                except Exception as e:
                    response.error.append({'num':num,'message':str(e)})
                    response.status = False
                    error_count +=1
                if error_count:
                    response.message = '共%s条,失败%s条' % (len(update_list), error_count,)
                else:
                    response.message = '更新成功'
            print(update_list)
        except Exception as e:
            response.status =False
            response.message = str(e)
        return response

