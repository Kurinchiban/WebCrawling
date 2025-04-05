import scrapy


class MitsubishiSpider(scrapy.Spider):
    name = "Mitsubishi"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Mitsubishi"]

    def parse(self, response):
        history = response.xpath('//table[@class="infobox ib-company vcard"]/following::p/text()').getall()
        data = {
            "History" : history,
        }
        return data 