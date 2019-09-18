"""
연결된 DB에

"""
import configs
from api.model.sqlalchemy import base


print("loading config...")

config = configs.from_arg_module()
uri = config["DATABASE_URI"]

print("configuring database...")

base.create_db(uri)

print("success!")