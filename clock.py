from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log,signals
from webreg_scrapy.spiders.course_spider import CourseSpider
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig()
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
    spider =CourseSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configured
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()