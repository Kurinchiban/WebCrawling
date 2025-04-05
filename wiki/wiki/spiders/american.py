import scrapy


class AmericanSpider(scrapy.Spider):
    name = "american"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/American_Express"]

    def parse(self, response):
        history = response.xpath('//figure[@class="mw-default-size"]/following::p/text()').getall()
        data = {
            "History" : history,
        }
        return data 