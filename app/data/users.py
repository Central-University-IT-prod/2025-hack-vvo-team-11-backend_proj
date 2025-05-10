import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True)
