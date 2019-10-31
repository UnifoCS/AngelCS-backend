import configs

#
# Put Your Debug Config here!!!
# See parameters at configs/__init__.py
class TestConfig(configs.DefaultConfig):
    DEBUG = True
    DATABASE_ECHO = False
    DATABASE_URI = "sqlite:///tmp/sqlite3.db"