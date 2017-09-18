import json
from utils.pager import PageInfo
from django.db.models import Q
from utils.response import BaseResponse
from django.http.request import QueryDict
from base.service.base import BaseServiceList
from helpdesk import models
class Server(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'status', 'text': '状态', 'condition_type': 'select', 'global_name': 'device_status_list'},
            {'name': 'user__username', 'text': '用户', 'condition_type': 'select', 'global_name': 'username_list'},
            {'name': 'user__computer', 'text': '公司', 'condition_type': 'select', 'global_name': 'computer_list'},
        ]

        table_config = [
            {
                'q': 'nid',
                'title': 'id',
                'display': 0,
                'text': {},
                'attr': {}
            },
            {
                'q': 'sn',
                'title': 'SN序列号',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@sn'}},
                'attr': {'name':'sn','id':'@sn','origin': '@sn', 'edit-enable': 'true','edit-type': 'input'}
            },
            # '{n}-{m}'.format({'n': 'hostname','m':'@hostname'}) => hostname-c1.com
            {
                'q': 'type',
                'title': '种类',
                'display': 1,
                #    'text':{},
                #     'attr':{}
                'text': {'content': '{m}', 'kwargs': {'m': '@type'}},
                'attr': {'name':'type','id':'@type','origin': '@type', 'edit-enable': 'true','edit-type': 'select',
                         'global-name': 'type_status_list'}
            },
            {
                'q': 'asset_model__name',
                'title': '型号',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@@asset_model_list'}},
                'attr': {'name':'int_ip','id':'@asset_model__name','origin': '@int_ip', 'edit-enable': 'true',
                         'edit-type': 'select','global-name': 'asset_model_list'}
            },
            {
                'q': 'status',
                'title': '状态',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@@device_status_list'}},
                'attr': {'name':'status','id':'@status','orginal': '@status', 'edit-enable': 'true', 'edit-type': 'select',
                         'global-name': 'device_status_list'}
            },
            {
                'q': 'user__username',
                'title': '用户',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@@username_list'}},
                'attr': {'name': 'user__username', 'id': '@user__username', 'orginal': '@user__username', 'edit-enable': 'true',
                         'edit-type': 'select','global-name': 'username_list'}
            },
            {
                'q': 'ipaddress',
                'title': '当前IP地址',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@ipaddress'}},
                'attr': {'name': 'ipaddress', 'id': '@ipaddress', 'orginal': '@ipaddress', 'edit-enable': 'false',}
            },
            {
                'q': 'user__computer',
                'title': '公司',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@@computer_list'}},
                'attr': {'name': 'user__computer', 'id': '@user__computer', 'orginal': '@user__computer', 'edit-enable': 'true',
                         'edit-type': 'select', 'global-name': 'computer_list'}
            },
        ]
        extra_select ={}
        super(Server, self).__init__(condition_config, table_config, extra_select)
    @property
    def device_status_list(self):
        result = map(lambda x:{'id':x[0],'name':x[1]},models.Asset.status_choices)
        return list(result)
    @property
    def computer_list(self):
        result = map(lambda x:{'id':x[0],'name':x[1]},models.Member.computer_choices)
        return list(result)
    @property
    def username_list(self):
        values=models.Member.objects.all.values('nid','username')
        return list(values)
    @property
    def asset_model_list(self):
        values = models.asset_model.objects.all.values('nid','name')
        return list(values)



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

            asset_count = models.Asset.objects.filter(conditions).count()
           # print(asset_count,'count',request.GET.get('pager')  )
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
                'device_status_list':self.device_status_list,
                'username_list': self.username_list,
                'computer_list': self.computer_list,
                'asset_model_list': self.asset_model_list
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

