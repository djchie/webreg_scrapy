from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_all_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Course(DeclarativeBase):
    """Sqlalchemy course model"""
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, nullable=False)
    number = Column('number', String, nullable=False)
    title = Column('title', String, nullable=False)
    deptName = Column('department_name', String, nullable=False)
    deptCode = Column('department_code', String, nullable=False)
    sessions = relationship('Session', backref='course')

# DEFINE SESSIONS TABLE
# MAKE SURE THE RELATIONSHIP IS CORRECT WITH COURSES
# IMPLEMENT THE INSERTION INTO THE DATABASE
class Session(DeclarativeBase):
    """Sqlalchemy session model"""
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column('course_id', Integer, ForeignKey('course.id'), nullable=False)
    code = Column('code', String, nullable=False)
    type = Column('type', String)
    section = Column('section', String)
    units = Column('units', String)
    instructor = Column('instructor', String)
    instructor2 = Column('instructor_2', String)
    time = Column('time', String)
    time2 = Column('time_2', String)
    location = Column('location', String)
    location2 = Column('location_2', String)
    final = Column('final', String)
    maximumEnrollmentAllowed = Column('maximum_enrollment_allowed', Integer)
    currentEnrollmentCount = Column('current_enrollment_count', String)
    currentWaitlistCount = Column('current_waitlist_count', String)
    enrollmentRequests = Column('enrollment_requests', Integer)
    enrollmentRestrictions = Column('enrollment_restrictions', String)
    textbookLink = Column('textbook_link', String)
    courseWebsite = Column('course_website', String)
    status = Column('status', String)














