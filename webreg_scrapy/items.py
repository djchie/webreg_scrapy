# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CourseItem(scrapy.Item):
    number = scrapy.Field()
    title = scrapy.Field()
    deptTitle = scrapy.Field()
    department = scrapy.Field()
    sessions = scrapy.Field()
    pass

class SessionItem(scrapy.Item):
    code = scrapy.Field()
    type = scrapy.Field()
    section = scrapy.Field()
    units = scrapy.Field()
    instructor = scrapy.Field()
    instructor2 = scrapy.Field()
    day = scrapy.Field()
    time = scrapy.Field()
    day2 = scrapy.Field()
    time2 = scrapy.Field()
    location = scrapy.Field()
    location2 = scrapy.Field()
    # final = scrapy.Field()
    maximumEnrollmentAllowed = scrapy.Field()
    currentEnrollmentCount = scrapy.Field()
    currentWaitlistCount = scrapy.Field()
    enrollmentRequests = scrapy.Field()
    enrollmentRestrictions = scrapy.Field()
    textbookLink = scrapy.Field()
    courseWebsite = scrapy.Field()
    status = scrapy.Field()
    pass

class DepartmentItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    pass