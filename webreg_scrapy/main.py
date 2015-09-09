from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from ..spiders.department_spider import DepartmentSpider
from spiders.course_spider import CourseSpider

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(DepartmentSpider)
    yield runner.crawl(CourseSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished