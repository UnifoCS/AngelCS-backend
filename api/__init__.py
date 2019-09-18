import logging
import os

from flask import Flask

import configs



class App:
    flask = Flask(__name__)

    def __init__(self):
        self.config = configs.from_arg_module()
        self.flask.config.from_object(self.config)
        self.init_logging()
        self.load_services()
        self.load_views()
        

    def init_logging(self):
        pass


    def load_services(self):
        pass


    def load_views(self):
        """
        api.view 패키지에 있는 모듈에서 bp라는 이름의 Blueprint 값을 가져와 
        Flask에 등록합니다.
        """
        modules = os.listdir('api/view')
        modules = filter(lambda x: x.endswith(".py"), modules)
        modules = map(lambda x: x[:-3], modules)

        for module_path in modules:
            mod = __import__(f"api.view.{module_path}", fromlist=["api.view"])
            if not hasattr(mod, "bp"):
                continue
            
            bp = getattr(mod, "bp")

            self.flask.register_blueprint(bp)


    def run(self):
        self.flask.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEBUG
        )