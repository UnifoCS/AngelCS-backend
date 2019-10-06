"""
연결된 DB에 테이블을 생성합니다.
사용법

> python init_db.py

"""
import sqlalchemy

import configs
from api.model.sqlalchemy import Base


print("loading config...")

config = configs.from_arg_module()
uri = config["DATABASE_URI"]
echo = config["DATABASE_ECHO"]

print("configuring database...")

engine = sqlalchemy.create_engine(uri, echo=echo)
Base.metadata.create_all(engine)

print("success!")