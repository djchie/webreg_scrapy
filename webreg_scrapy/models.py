from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine.url import URL
from datetime import datetime

import sys, settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # print '=================== WHAT ENV IS IT?? ===================='
    # print sys.argv[sys.argv.length - 1]
    return create_engine(URL(**settings.DEVELOPMENT_DATABASE))


def create_all_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

def drop_all_tables(engine):
    """"""
    DeclarativeBase.metadata.drop_all(engine)

def _get_date():
    return datetime.now()

class Course(DeclarativeBase):
    """Sqlalchemy course model"""
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    deptTitle = Column('department_title', String, nullable=False)
    department = Column('department', String, nullable=False)
    number = Column('number', String, nullable=False)
    title = Column('title', String, nullable=False)
    sessions = relationship('Session', backref='course')
    createdAt = Column('created_at', Date, default=_get_date)
    updatedAt = Column('updated_at', Date, default=_get_date, onupdate=_get_date)

class Session(DeclarativeBase):
    """Sqlalchemy session model"""
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    course_id = Column('course_id', Integer, ForeignKey('course.id'), nullable=False)
    code = Column('code', String, nullable=False)
    type = Column('type', String, default='N/A')
    section = Column('section', String, default='N/A')
    units = Column('units', String, default='N/A')
    instructor = Column('instructor', String, default='N/A')
    instructor2 = Column('instructor_2', String, default='N/A')
    day = Column('day', String, default='N/A')
    time = Column('time', String, default='N/A')
    day2 = Column('day_2', String, default='N/A')
    time2 = Column('time_2', String, default='N/A')
    location = Column('location', String, default='N/A')
    location2 = Column('location_2', String, default='N/A')
    final = Column('final', String, default='N/A')
    maximumEnrollmentAllowed = Column('maximum_enrollment_allowed', String, default='N/A')
    currentEnrollmentCount = Column('current_enrollment_count', String, default='N/A')
    currentWaitlistCount = Column('current_waitlist_count', String, default='N/A')
    enrollmentRequests = Column('enrollment_requests', String, default='N/A')
    enrollmentRestrictions = Column('enrollment_restrictions', String, default='N/A')
    textbookLink = Column('textbook_link', String, default='N/A')
    courseWebsite = Column('course_website', String, default='N/A')
    status = Column('status', String, default='N/A')
    createdAt = Column('created_at', Date, default=_get_date)
    updatedAt = Column('updated_at', Date, onupdate=_get_date)














