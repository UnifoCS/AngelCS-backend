
class BaseService(object):
    __ignore__ = False
    __ignore_subclass__ = False
    

    def __init__(self, app):
        self.app = app
    
    def __del__(self):
        pass
