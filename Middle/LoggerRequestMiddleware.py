from Middle.base import CrequestMiddleware
from fintch.logger import access_log as logger
from utils import windows_log
class UserAction(CrequestMiddleware):
    def process_request(self,request):
        super(UserAction,self).process_request(request)

    def process_response(self, request, response):
        print('process_response')

        super(UserAction, self).process_response(request, response)
        return response

    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
       # logger = windows_log.syslog("remote-host-name")
        message = '{} {} {} {} {} {}'.format(request.user, request.method, request.path,view_func.view_class,view_func_args,view_func_kwargs)


        #log.send(message,windows_log.Level.WARNING)
        #print('view_log')
        logger.info(message)  ###用户访问记录

    def process_exception(self, request, exception):
        super(UserAction, self).process_exception(request, exception)
        print('process_exception')
