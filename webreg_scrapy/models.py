from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_courses_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Courses(DeclarativeBase):
    """Sqlalchemy courses model"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    course_number = Column('course_number', String)
    course_name = Column('course_name', String)
    department_name = Column('department_name', String)
    department_code = Column('department_code', String)

class Sessions(DeclarativeBase):
    """Sqlalchemy sessions model"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    course_number = Column('course_number', String)
    course_name = Column('course_name', String)
    department_name = Column('department_name', String)
    department_code = Column('department_code', String)