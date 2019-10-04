
import os
import argparse

#
# release, debug 외에 다른 config를 여기에 추가
def from_arg_module():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="debug", type=str)
    args = parser.parse_args()

    config = args.config

    if config == "release":
        from . import release
        return release.ReleaseConfig()

    elif config == "debug":
        from . import debug
        return debug.DebugConfig()

    else:
        return DefaultConfig()


class DefaultConfig(dict):
    APP_NAME = "angelcs_api"
    
    DEBUG = False
    HOST = "0.0.0.0"  # 0.0.0.0 to public
    PORT = 8080         # port number

    # 
    # See SQLAlchemy URI Format
    DATABASE_ECHO = False
    DATABASE_URI = "sqlite:///tmp/sqlite3.db"

    # SQLALCHEMY Configs


    # Log Level
    # see logging level details at [URL]
    LOG_LEVEL = "INFO"
    LOG_FILE = f"./log/{APP_NAME}.log"


    # Configurations를 JSON에서 불러옵니다.
    def load_from_json(self, filename):
        import json
        obj = json.load(filename)

        for k, v in obj.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
             return None
