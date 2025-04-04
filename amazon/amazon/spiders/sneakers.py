import scrapy
from datetime import datetime


class SneakersSpider(scrapy.Spider):
    name = 'sneakers'
    domain = "https://www.amazon.in"
    allowed_domains = ['www.amazon.in']
    start_urls = ['https://www.amazon.in/s?k=sneakers+for+men&crid=1E5W5JQ3J1G46&sprefix=sn%2Caps%2C207&ref=nb_sb_ss_ts-doa-p_1_2']

    def parse(self, response):

        # Listing Page Logic

        product_urls = response.xpath('//a[@class="a-link-normal s-no-outline"]/@href').getall()
        for product_url in product_urls:
            product_url = self.domain + product_url
            yield response.follow(url=product_url,callback=self.parse_product_page)

        # Next Page Logic 

        next_page_url = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
        if next_page_url:
            next_page_url = self.domain + next_page_url
            yield response.follow(url=next_page_url,callback=self.parse) 

    
    def parse_product_page(self, response):

        # Product Page Logic
        
        title = response.xpath('//span[@id="productTitle"]/text()').get()
        rating = response.xpath('//a[@class="a-popover-trigger a-declarative"]/span[@class="a-size-base a-color-base"]/text()').get()
        price = response.xpath('//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]/span[@class="a-offscreen"]/text()').get()
        image = response.xpath('').getall()
        size = response.xpath('//option[@class="dropdownSelect" or @class="dropdownAvailable" or @class="dropdownUnavailable"]/text()').getall()

        description_1 = response.xpath('//ul[@class="a-unordered-list a-vertical a-spacing-mini"]/li//text()').getall()
        description_2 = response.xpath('//ul[@class="a-unordered-list a-vertical a-spacing-none"]/li//text()').getall()


        yield {
            'crawlDate':  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'statusCode': str(response.status),
            'id': response.url,

            'title':title,
            'rating':rating,
            'price': price,
            'size': size,
            'image': image,
            'description': description_1 + description_2

        }