import scrapy
from pep_parse.items import PepParseItem
import re


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        urls_list = response.css('section[id="numerical-index"] tr')
        for url in urls_list:
            pep_url = url.css("td a::attr(href)").get()
            if pep_url is not None:
                yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, response):
        full_name = response.css("h1.page-title::text").get()
        pep_name_match = re.search(r'PEP (\d+) – (.+)', full_name)
        pep_number, pep_name = pep_name_match.groups()
        pep_status = response.css('dt:contains("Status:") + dd'
                                  ).css("abbr::text").get()

        item = PepParseItem()
        item['number'] = pep_number
        item['name'] = pep_name.strip()
        item['status'] = pep_status

        yield item
