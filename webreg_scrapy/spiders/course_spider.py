import scrapy
import re
import string
import time

from scrapy.http import FormRequest, Request
from webreg_scrapy.items import DepartmentItem, CourseItem, SessionItem

class DepartmentSpider(scrapy.Spider):
    name = "course_scrapy"
    allowed_domains = ["reg.uci.edu"]
    start_urls = [
        "https://www.reg.uci.edu/perl/WebSoc"
    ]
    CONCURRENT_REQUESTS = 1
    DOWNLOAD_DELAY = 3

    def start_requests(self):
        yield Request(url="https://www.reg.uci.edu/perl/WebSoc",
                    callback=self.parse_departments)

    def parse_departments(self, response):
        # For testing out a single page
        # yield FormRequest("https://www.reg.uci.edu/perl/WebSoc",
        #         formdata={'YearTerm': '2015-92', 'Dept': 'SOCECOL'},
        #         callback=self.parse_courses,
        #         meta={
        #             'departmentCode': 'SOCECOL',
        #             'departmentName': 'Social Ecology'
        #         })
        for departmentXML in response.xpath('//select[@name="Dept"]/option'):
            department = DepartmentItem()
            department['code'] = departmentXML.xpath('@value').extract()[0].replace(u"\u00A0", " ").strip()
            lastPeriodIndex = departmentXML.xpath('text()').extract()[0].replace(u"\u00A0", " ").rfind('.')
            department['name'] = departmentXML.xpath('text()').extract()[0].replace(u"\u00A0", " ")[lastPeriodIndex + 1:].strip()
            if (department['code'] != 'ALL'):
                # UPDATE POINTS: YearTerm
                yield FormRequest("https://www.reg.uci.edu/perl/WebSoc",
                    formdata={'YearTerm': '2015-92', 'Dept': department['code']},
                    callback=self.parse_courses,
                    meta={
                        'departmentCode': department['code'],
                        'departmentName': department['name']
                    })

    def parse_courses(self, response):
        blueBarCount = 0
        # For testing
        # print 'DEPARTMENT === ' + response.meta['departmentCode']
        # print 'TIME === ' + time.asctime()
        for courseXML in response.xpath('//tr[@bgcolor="#fff0ff"]'):
            course = CourseItem()
            course['courseNumber'] = re.sub(' +', ' ', courseXML.xpath('td[@class="CourseTitle"]/text()[1]').extract()[0].replace(u"\u00A0", " ").strip()
            # For testing
            print 'COURSE NUMBER === ' + course['courseNumber']
            course['courseName'] = string.capwords(courseXML.xpath('td[@class="CourseTitle"]/font/b/text()').extract()[0])
            course['departmentName'] = response.meta['departmentName']
            course['departmentCode'] = response.meta['departmentCode']

            sessions = []
            for sessionXML in courseXML.xpath('following-sibling::tr[@valign="top" and count(preceding-sibling::tr[@class="blue-bar"])=' + str(blueBarCount) + ']'):
                session = SessionItem()
                session['code'] = sessionXML.xpath('td[1]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                # For testing
                print 'SESSION CODE === ' + session['code']
                session['type'] = sessionXML.xpath('td[2]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                session['section'] = sessionXML.xpath('td[3]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                session['units'] = sessionXML.xpath('td[4]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                session['instructor'] = sessionXML.xpath('td[5]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                # Needed to handle when there's two instructors
                if len(sessionXML.xpath('td[5]/text()')) == 2:
                    session['instructor2'] = sessionXML.xpath('td[5]/text()').extract()[1].replace(u"\u00A0", " ").strip()
                session['time'] = sessionXML.xpath('td[6]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                # Needed to handle when there's two times
                if len(sessionXML.xpath('td[6]/text()')) == 2:
                    session['time2'] = sessionXML.xpath('td[6]/text()').extract()[1].replace(u"\u00A0", " ").strip()

                # Needed to handle when it's just TBA
                if len(sessionXML.xpath('td[7]/a')) >= 1:
                    session['location'] = sessionXML.xpath('td[7]/a/text()').extract()[0].replace(u"\u00A0", " ").strip()
                    # Needed to handle when there's two locations, so there's two a links
                    if len(sessionXML.xpath('td[7]/a')) == 2:
                        session['location2'] = sessionXML.xpath('td[7]/a/text()').extract()[1].replace(u"\u00A0", " ").strip()
                        
                    # Essentially, change the parameter for greater than 1
                    # Add the first one, and then add the second one to a second location column
                    # Need to do the same for time, but understand time is still under one div
                    # Basically delimit on that space, print out the time first to see what to delimit
                    # Handle when there's two professors as well
                else:
                    session['location'] = sessionXML.xpath('td[7]/text()').extract()[0].replace(u"\u00A0", " ").strip()

                # For some reason, the final part for index 8 is getting skipped over, so skip it for now and
                # continue on index 8. I think it's just ignoring the <td nowrap="nowrap"></td>
                # session['final'] = sessionXML.xpath('td[8]/text()').extract()[0].replace(u"\u00A0", " ")
                # print session['final']

                session['maximumEnrollmentAllowed'] = sessionXML.xpath('td[8]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                session['currentEnrollmentCount'] = sessionXML.xpath('td[9]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                session['currentWaitlistCount'] = sessionXML.xpath('td[10]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                session['enrollmentRequests'] = sessionXML.xpath('td[11]/text()').extract()[0].replace(u"\u00A0", " ").strip()
                session['enrollmentRestrictions'] = sessionXML.xpath('td[12]/text()').extract()[0].replace(u"\u00A0", " ").strip()

                if len(sessionXML.xpath('td[13]/a')) == 1:
                    session['textbookLink'] = sessionXML.xpath('td[13]/a/@href').extract()[0].replace(u"\u00A0", " ").strip()
                else:
                    session['textbookLink'] = ""

                if len(sessionXML.xpath('td[14]/a')) == 1:
                    session['courseWebsite'] = sessionXML.xpath('td[14]/a/@href').extract()[0].replace(u"\u00A0", " ").strip()
                else:
                    session['courseWebsite'] = ""

                if len(sessionXML.xpath('td[15]/b/font')) == 1:
                    session['status'] = sessionXML.xpath('td[15]/b/font/text()').extract()[0].replace(u"\u00A0", " ").strip()
                elif len(sessionXML.xpath('td[15]/font')):
                    session['status'] = sessionXML.xpath('td[15]/font/text()').extract()[0].replace(u"\u00A0", " ").strip()
                else:
                    session['status'] = sessionXML.xpath('td[15]/text()').extract()[0].replace(u"\u00A0", " ").strip()

                sessions.append(session)
            course['sessions'] = sessions
            blueBarCount += 1
            yield course
