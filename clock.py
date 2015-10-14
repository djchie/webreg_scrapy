# import scrapy
# from scrapy.crawler import CrawlerProcess
# from webreg_scrapy.spiders.course_spider import CourseSpider
# from apscheduler.schedulers.blocking import BlockingScheduler
# import logging

# logging.basicConfig()
# sched = BlockingScheduler()

# @sched.scheduled_job('interval', seconds=5)
# def timed_job():
#     print('This job is run every three minutes.')
#     process = CrawlerProcess()
#     process.crawl(CourseSpider)
#     process.start() # the script will block here until the crawling is finished

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

# sched.start()




from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log,signals
from webreg_scrapy.spiders.course_spider import CourseSpider
from scrapy.utils.project import get_project_settings
import logging
logging.basicConfig()

# def run():
#     spider = CourseSpider()
#     settings = get_project_settings()
#     crawler = Crawler(settings)
#     crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
#     crawler.configured
#     crawler.crawl(spider)
#     crawler.start()
#     log.start()
#     reactor.run()


# from apscheduler.schedulers.twisted import TwistedScheduler
# sched = TwistedScheduler()
# sched.add_job(run, 'interval', seconds=1)
# sched.start()




from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=1)
def timed_job():
    spider = CourseSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configured
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()

sched.start()