import scrapy


class WiproSpider(scrapy.Spider):
    name = "wipro"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Wipro"]

    def parse(self, response):
        history = response.xpath('//table[@class="infobox ib-company vcard"]/following::p/text()').getall()
        data = {
            "History" : history,
        }
        return data 