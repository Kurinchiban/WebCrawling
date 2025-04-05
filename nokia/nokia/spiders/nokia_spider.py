import scrapy
from datetime import datetime

class NokiaSpiderSpider(scrapy.Spider):
    name = "nokia_spider"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=nokia&crid=2YW1HSQVTF4RL&sprefix=nokia%2Caps%2C225&ref=nb_sb_ss_pltr-data-refreshed_3_5"]

    def parse(self, response):
        
        # Listing Page Logic

        product_urls = response.xpath(
            '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').getall()
        for product_url in product_urls:
            product_url = 'https://www.amazon.in' + product_url
            yield response.follow(
            url=product_url,
            callback=self.parse_product_page,
            headers = {
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ta;q=0.6",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

        )
        # Next Page Logic

        next_page_url = response.xpath(
            "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
        if next_page_url:
            next_page_url = 'https://www.amazon.in' + next_page_url
            yield response.follow(
            url=next_page_url,
            callback=self.parse,
            headers = {
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ta;q=0.6",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }
        )

    def parse_product_page(self, response):

        # Product Page Logic

        name = response.xpath(
            "//span[@class='a-size-large product-title-word-break']/text()").get()
        price = response.xpath("//span[@class='a-price-whole']/text()").get()

        specification = {}
        specs = response.xpath(
            "//table[@class='a-normal a-spacing-micro']/tr")
        for spec in specs:
            key = spec.xpath(".//td[@class='a-span3']/span/text()").get()
            value = spec.xpath(".//td[@class='a-span9']/span/text()").get()
            if key and value:
                specification[key.strip()] = value.strip()
        if price:
            price = price.strip()
        
        yield {
            'Id': response.url,
            'Name': name.strip(),
            'Price': price,
            'Specification': specification,
            'crawlDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
