import json
from django.db.models import Q


class BaseServiceList(object):
    def __init__(self,condition_config,table_config,extra_select):
        # 查询条件的配置，列表
        self.condition_config = condition_config

        self.table_config = table_config

        self.extra_select = extra_select

    @property
    def values_list(self):
        values = []
        for item in self.table_config:
            if item['q']:
                values.append(item['q'])
        return values

    @staticmethod
    def assets_condition(request):
        con_str = request.GET.get('condition',None)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)
        con_q = Q()
        for k,v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k,item))
            con_q.add(temp,'ADD')
        return con_q



