import scrapy


class BakerSpider(scrapy.Spider):
    name = "baker"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Baker_Hughes"]

    def parse(self, response):
        history = response.xpath('//table[@class="infobox ib-company vcard"]/following::p/text()').getall()
        data = {
            "History" : history,
        }
        return data
