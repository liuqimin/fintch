
class BaseResponse(object):
    #self.__dict__ = [self.status,self.data,self.message]
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None