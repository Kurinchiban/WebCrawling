import scrapy


class McafeeSpider(scrapy.Spider):
    name = "mcafee"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/McAfee"]

    def parse(self, response):
        history = response.xpath('//figure[@class="mw-default-size"]/following::p/text()').getall()
        data = {
            "History" : history,
        }
        return data
