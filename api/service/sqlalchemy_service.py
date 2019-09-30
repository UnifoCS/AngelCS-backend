from . import BaseService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..model.sqlalchemy import Base


class SQLAlchemyService(BaseService):
    
    def __init__(self, app):
        super().__init__(app)
        self.engine = create_engine(app.config["DATABASE_URI"], echo=True)#echo=app.config.get("DATABASE_ECHO", False))
        self.session = scoped_session(sessionmaker(bind=self.engine))
        # Base.query = self.session.query_property()
        # self.session = Session()

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def drop_db(self):
        Base.metadata.drop_all(self.engine)


class BaseDatabaseService(BaseService):

    @property
    def db(self):
        return self.app.services.sql_alchemy.session

    def query(self, *vargs):
        return self.db.query(*vargs)

    def commit(self):
        self.db.commit()
