import scrapy
import re
import string

from scrapy.http import FormRequest, Request
from webreg_scrapy.items import DepartmentItem

class DepartmentSpider(scrapy.Spider):
    name = "department_scrapy"
    allowed_domains = ["https://www.reg.uci.edu"]
    start_urls = [
        "https://www.reg.uci.edu/perl/WebSoc"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'

        with open(filename, 'wb') as f:
            f.write(response.body)

        for departmentXML in response.xpath('//select[@name="Dept"]/option'):
            department = DepartmentItem()
            department['code'] = departmentXML.xpath('@value').extract()[0].replace(u"\u00A0", " ").strip()
            lastPeriodIndex = departmentXML.xpath('text()').extract()[0].replace(u"\u00A0", " ").rfind('.')
            department['name'] = departmentXML.xpath('text()').extract()[0].replace(u"\u00A0", " ")[lastPeriodIndex + 1:].strip()
            yield department



