import configs

#
# Put Your Debug Config here!!!
# See parameters at configs/__init__.py
class DebugConfig(configs.DefaultConfig):
    DEBUG = True
    DATABASE_ECHO = True
    DATABASE_URI = "sqlite:///tmp/sqlite3.db"