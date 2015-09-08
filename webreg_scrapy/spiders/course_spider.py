import scrapy
import re
import string

from scrapy.http import FormRequest, Request
from webreg_scrapy.items import CourseItem, SessionItem

class CourseSpider(scrapy.Spider):
    name = "course_scrapy"
    allowed_domains = ["https://www.reg.uci.edu"]

    # currentYearTerm = '2015-92'

    def start_requests(self):
        return [FormRequest(url="https://www.reg.uci.edu/perl/WebSoc",
                    formdata={'YearTerm': '2015-92', 'Dept': 'COMPSCI'},
                    callback=self.parse)]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'

        with open(filename, 'wb') as f:
            f.write(response.body)

        blueBarCount = 0

        for courseXML in response.xpath('//tr[@bgcolor="#fff0ff"]'):
            course = CourseItem()
            course['courseNumber'] = re.sub(' +', ' ', courseXML.xpath('td[@class="CourseTitle"]/text()[1]').extract()[0].replace(u"\u00A0", " ").strip())
            course['courseName'] = string.capwords(courseXML.xpath('td[@class="CourseTitle"]/font/b/text()').extract()[0])
            sessions = []

            for sessionXML in courseXML.xpath('following-sibling::tr[@valign="top" and count(preceding-sibling::tr[@class="blue-bar"])=' + str(blueBarCount) + ']'):
                session = SessionItem()
                session['courseCode'] = sessionXML.xpath('td[1]/text()').extract()[0].replace(u"\u00A0", " ")
                session['courseType'] = sessionXML.xpath('td[2]/text()').extract()[0].replace(u"\u00A0", " ")
                session['section'] = sessionXML.xpath('td[3]/text()').extract()[0].replace(u"\u00A0", " ")
                session['units'] = sessionXML.xpath('td[4]/text()').extract()[0].replace(u"\u00A0", " ")
                session['instructor'] = sessionXML.xpath('td[5]/text()').extract()[0].replace(u"\u00A0", " ")
                session['time'] = sessionXML.xpath('td[6]/text()').extract()[0].replace(u"\u00A0", " ")

                # Need to handle when it's just TBA
                if len(sessionXML.xpath('td[7]/a')) == 1:
                    session['place'] = sessionXML.xpath('td[7]/a/text()').extract()[0].replace(u"\u00A0", " ")
                else:
                    session['place'] = sessionXML.xpath('td[7]/text()').extract()[0].replace(u"\u00A0", " ")

                # For some reason, the final part for index 8 is getting skipped over, so skip it for now and
                # continue on index 8. I think it's just ignoring the <td nowrap="nowrap"></td>
                # session['final'] = sessionXML.xpath('td[8]/text()').extract()[0].replace(u"\u00A0", " ")
                # print session['final']

                session['maximumEnrollmentAllowed'] = sessionXML.xpath('td[8]/text()').extract()[0].replace(u"\u00A0", " ")
                session['currentEnrollmentCount'] = sessionXML.xpath('td[9]/text()').extract()[0].replace(u"\u00A0", " ")
                session['currentWaitlistCount'] = sessionXML.xpath('td[10]/text()').extract()[0].replace(u"\u00A0", " ")
                session['enrollmentRequests'] = sessionXML.xpath('td[11]/text()').extract()[0].replace(u"\u00A0", " ")
                session['reservedForNewStudentsCount'] = sessionXML.xpath('td[12]/text()').extract()[0].replace(u"\u00A0", " ")
                session['enrollmentRestrictions'] = sessionXML.xpath('td[13]/text()').extract()[0].replace(u"\u00A0", " ")

                if len(sessionXML.xpath('td[14]/a')) == 1:
                    session['textbookLink'] = sessionXML.xpath('td[14]/a/@href').extract()[0].replace(u"\u00A0", " ")
                else:
                    session['textbookLink'] = ""

                # For some reason, the courseWebsite for index 16 part is getting skipped over, so skip it for now and
                # continue on index 15. I think it's just ignoring the <td nowrap="nowrap"></td>
                # if len(sessionXML.xpath('td[15]/a')) == 1:
                #     session['courseWebsite'] = sessionXML.xpath('td[15]/a/text()').extract()[0].replace(u"\u00A0", " ")
                # else:
                #     session['courseWebsite'] = ""
                # print session['courseWebsite']

                if len(sessionXML.xpath('td[16]/b/font')) == 1:
                    session['status'] = sessionXML.xpath('td[16]/b/font/text()').extract()[0].replace(u"\u00A0", " ") 
                elif len(sessionXML.xpath('td[16]/font')):
                    session['status'] = sessionXML.xpath('td[16]/font/text()').extract()[0].replace(u"\u00A0", " ")
                else:
                    session['status'] = sessionXML.xpath('td[16]/text()').extract()[0].replace(u"\u00A0", " ")

                sessions.append(session)
            course['sessions'] = sessions
            blueBarCount += 1
            yield course




