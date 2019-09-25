from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from werkzeug.security import generate_password_hash, check_password_hash
from api.util.text import convert_camel_to_snake

Base = declarative_base()


class BaseModel():
    __mapper_args__= {'always_refresh': True}

    @declared_attr
    def __tablename__(cls):
        return convert_camel_to_snake(cls.__name__)


class IdMixin():
    id =  Column(Integer, primary_key=True, autoincrement=True)


class TimestampMixin():
    created_date = Column(DateTime, default=datetime.utcnow())
    updated_date = Column(DateTime, onupdate=datetime.utcnow())



class User(Base, BaseModel, IdMixin, TimestampMixin):
    name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)

    # get channels of this user
    channels = relationship('Channel', secondary='link_user_channel')

    #below our user model, we will create our hashing functions
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ReferenceUserMixin:
    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("user.id"), index=True, nullable=False)


class Channel(Base, BaseModel, IdMixin, TimestampMixin):
    name = Column(String(64), nullable=False)
    provider = Column(String(64), nullable=False)

    # get all templates of user's specific template
    # templates = relationship("Template", backref="template")

    # get all users who has this channel
    users = relationship('User', secondary='link_user_channel')

    # get all reviews of this channel
    reviews = relationship("Review", backref="channel")

class ReferenceChannelMixin():
    @declared_attr
    def channel_id(cls):
        return Column(Integer, ForeignKey("channel.id"), index=True, nullable=False)


class LinkUserChannel(Base, BaseModel, IdMixin):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channel.id'), nullable=False)
    __table_args__ = (
        Index('index_user_channel_id', user_id, channel_id, unique=True),
    )


class Review(Base, BaseModel, IdMixin, TimestampMixin, ReferenceChannelMixin):
    title = Column(String(64), nullable=False)
    content = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False, index=True)

    # get tags of this review
    tags = relationship('Tag', secondary='link_review_tag')

class ReferenceReviewMixin():
    @declared_attr
    def review_id(cls):
        return Column(Integer, ForeignKey("review.id"), index=True)



class Tag(Base, BaseModel, IdMixin, TimestampMixin):
    name = Column(String(32), nullable=False)
    
    reviews = relationship('Tag', secondary='link_review_tag')

class LinkReviewTag(Base, BaseModel, IdMixin):
    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)

    __table_args__ = (
        Index('index_link_review_tag', review_id, tag_id, unique=True),
    )



class Template(Base, BaseModel, IdMixin, TimestampMixin, ReferenceChannelMixin):
    name = Column(String(32), nullable=False)
    content = Column(String, nullable=False)

    conditions = relationship("TemplateCondition", backref="template")

class ReferenceTemplateMixin():
    @declared_attr
    def template_id(cls):
        return Column(Integer, ForeignKey("template.id"), index=True, nullable=False)

class TemplateCondition(Base, BaseModel, IdMixin, ReferenceTemplateMixin):
    index = Column(Integer, index=True)
    operand1 = Column(String)
    operand2 = Column(String)
    operator = Column(String(16), nullable=False)