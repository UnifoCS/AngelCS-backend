from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from api.util.text import convert_camel_to_snake

Base = declarative_base()


class BaseModel():
    __mapper_args__= {'always_refresh': True}

    @declared_attr
    def __tablename__(cls):
        return convert_camel_to_snake(cls.__name__)


class IdMixin():
    id =  Column(Integer, primary_key=True, auto_increament=True)


class TimestampMixin():
    created_date = Column(DateTime, default=datetime.utcnow())
    updated_date = Column(DateTime, onupdate=datetime.utcnow())



class User(Base, BaseModel, IdMixin, TimestampMixin):
    name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)

    # get all channels of this user
    channels = relationship("Channel", backref="user")

    #below our user model, we will create our hashing functions
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ReferenceUserMixin:
    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("user.id"), index=True)


class Channel(Base, BaseModel, IdMixin, TimestampMixin):
    name = Column(String(64), nullable=False)
    provider = Column(String(64), nullable=False)

    # get all templates of user's specific template
    # templates = relationship("Template", backref="template")

    # get all reviews of this channel
    reviews = relationship("Review", backref="channel")

class ReferenceChannelMixin():
    @declared_attr
    def channel_id(cls):
        return Column(Integer, ForeignKey("channel.id"))



class Review(Base, BaseModel, IdMixin, TimestampMixin, ReferenceUserMixin):
    title = Column(String(64), nullable=False)
    content = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False, index=True)

    # get tags of this review
    tags = relationship("Tag", backref="review")
    
class ReferenceReviewMixin():
    @declared_attr
    def review_id(cls):
        return Column(Integer, ForeignKey("review.id"))



class Tag(Base, BaseModel, IdMixin, TimestampMixin, ReferenceReviewMixin):
    name = Column(String(32), nullable=False)


class Template(Base, BaseModel, IdMixin, TimestampMixin, ReferenceChannelMixin):
    name = Column(String(32), nullable=False)
    content = Column(String, nullable=False)

    conditions = relationship("TemplateCondition", backref="template")

class ReferenceTemplateMixin():
    @declared_attr
    def template_id(cls):
        return Column(Integer, ForeignKey("template.id"))

class TemplateCondition(Base, BaseModel, IdMixin, ReferenceTemplateMixin):
    index = Column(Integer, index=True)
    operand1 = Column(String)
    operand2 = Column(String)
    operator = Column(String(16), nullable=False)