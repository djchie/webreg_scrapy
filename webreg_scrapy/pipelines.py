# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Course, Session, db_connect, create_all_tables, drop_all_tables

class WebregScrapyPipeline(object):
    """WebregScrapy pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates course and session table.
        """
        engine = db_connect()
        # TODO: Refer to the TODO below to avoid using the line below
        drop_all_tables(engine)
        create_all_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save courses and sessions in the database.

        This method is called for every item pipeline component.

        """

        # TODO: Find a way to update rather than over write all the data
        db_session = self.Session()

        course_data = {'number': item['number'], 
                       'title': item['title'], 
                       'deptName': item['deptName'], 
                       'deptCode': item['deptCode']}
        course = Course(**course_data)

        sessions_data = item['sessions']
        for session_data in sessions_data:
            session = Session(**session_data)
            course.sessions.append(session)

        try:
            db_session.add(course)
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()

        return item
