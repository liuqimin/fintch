import json
from utils.pager import PageInfo
from django.db.models import Q
from utils.response import BaseResponse
from django.http.request import QueryDict
from base.service.base import BaseServiceList
from helpdesk import models
from django.forms.models import model_to_dict
class Asset(BaseServiceList):
    def __init__(self):
        condition_config = [
            { 'text': '条件筛选', 'condition_type': 'input'},
            {'name': 'status', 'text': '状态', 'condition_type': 'select', 'global_name': 'device_status_list'},
            {'name': 'user_id', 'text': '用户', 'condition_type': 'select', 'global_name': 'username_list'},
            {'name': 'user__computer', 'text': '公司', 'condition_type': 'select', 'global_name': 'computer_list'},
        ]

        table_config = [
            {
                'q': 'ni',
                'title': 'id',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@ni'}},
                'attr': {'name':'sn'}
            },
            {
                'q': 'sn',
                'title': 'SN序列号',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@sn'}},
                'attr': {'name':'sn','id':'@sn','origin': '@sn', 'edit-enable': 'false'}
            },
            # '{n}-{m}'.format({'n': 'hostname','m':'@hostname'}) => hostname-c1.com
            {
                'q': 'type',
                'title': '种类',
                'display': 1,
                #    'text':{},
                #     'attr':{}
                'text': {'content': '{m}', 'kwargs': {'m': '@@type_list'}},
                'attr': {'name':'type','id':'@type','origin': '@type', 'edit-enable': 'true','edit-type': 'select',
                         'global-name': 'type_list'}
            },
            {
                'q': 'asset_model__name',
                'title': '型号',
                'display': 1,
                'text': {'content': '{m}', 'kwargs': {'m': '@asset_model__name'}},
                'attr': {'name':'asset_model','id':'@asset_model','origin': '@asset_model', 'edit-enable': 'true',
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
                'text': {'content': '{m}', 'kwargs': {'m': '@user__username'}},
                'attr': {'name': 'user', 'id': '@user', 'orginal': '@user', 'edit-enable': 'true',
                         'edit-type': 'select','global-name': 'username_list'}
            },
            {
                'q': 'user',
                'title': '用户',
                'display': 0,
            },
            {
                'q': 'asset_model',
                'title': '型号',
                'display': 0,
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
        super(Asset, self).__init__(condition_config, table_config, extra_select)
    @property
    def type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.type_choices)
        return list(result)

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
        values=models.Member.objects.all().values('nid','username')
        result = map(lambda x:{'id':x[0],'name':x[1]},values)
        values = models.Member.objects.only('nid', 'username')
        result = map(lambda x: {'id': x.nid, 'name': x.username}, values)
        return list(result)

    @property
    def asset_model_list(self):
        values = models.asset_model.objects.all().values('nid','name').values_list()
        result = map(lambda x: {'id': x[0], 'name': x[1]}, values)
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

    def fetch_asset(self,request):
        response = BaseResponse()

        try:
            ret = {}
            print(request)
            conditions = self.Server_condition(request)
            print(conditions)
            asset_count = models.Asset.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager',None),asset_count)
            asset_list = models.Asset.objects.filter(conditions).extra(select=self.extra_select)\
                             .values(*self.values_list)[page_info.start:page_info.end]
            print(asset_list)
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
                'asset_model_list': self.asset_model_list,
                'type_list':self.type_list,
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
            print(delete_dict)
            print(id_list)
            models.Asset.objects.filter(id__in=id_list).delete()
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
            print(put_dict)
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

