import logging
import os
import types

from flask import Flask, g
from flask_cors import CORS

import configs
from .util.text import convert_camel_to_snake
from .util.encoder import CustomJSONEncoder


class App:
    flask = Flask(__name__)
    services = types.SimpleNamespace()

    def __init__(self, config=configs.from_arg_module()):
        CORS(self.flask)
        
        self.config = config
        self.flask.config.from_object(self.config)
        self.flask.json_encoder = CustomJSONEncoder
        self.init_logging()
        self.load_services()
        self.load_views()

        from . import globals
        globals.init(self)

    def init_logging(self):
        logging.basicConfig(filename=self.config["LOG_FILE"],level=self.config["LOG_LEVEL"])

        handler = logging.StreamHandler()
        logger = logging.getLogger()
        logger.addHandler(handler)




    def load_services(self):
        from .service import BaseService

        modules = os.listdir('api/service')
        modules = filter(lambda x: x.endswith(".py"), modules)
        modules = map(lambda x: x[:-3], modules)

        for module_path in modules:
            mod = __import__(f"api.service.{module_path}", fromlist=["api.service"])
            # logging.debug(f"Load Service Module {module_path}")

        for sub in BaseService.__subclasses__():
            self.register_service(sub)


    def register_service(self, cls):
        # logging.debug(f"register_service({cls.__name__})")
        name = cls.__name__
        snake_name = convert_camel_to_snake(name)

        if snake_name.endswith("_service"):
            snake_name = snake_name[:-len("_service")]
        ins = cls(self)

        # __ignore__ = True면 무시합니다.
        # snake_name이 base_ 로 시작하면 등록하지 않습니다.
        if not ins.__ignore__ and not snake_name.startswith("base_"):
            logging.debug(f"Create Service: {name} -> {snake_name}")
            setattr(self.services, snake_name, ins)

        # __ignore_subclass__ = True면 서브클래스 등록 안함.
        if not ins.__ignore_subclass__:        
            # 자식 클래스들도 등록합니다.
            for sub in cls.__subclasses__():
                self.register_service(sub)


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

            logging.debug(f"Load View {module_path}")


    def run(self):
        self.flask.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEBUG
        )