from . import BaseService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQLAlchemyService(BaseService):
    
    def __init__(self, app):
        super().__init__(app)
        self.engine = create_engine(app.config["DATABASE_URI"])
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


class BaseDatabaseService(BaseService):

    @property
    def db(self):
        return self.app.services.sql_alchemy.session
