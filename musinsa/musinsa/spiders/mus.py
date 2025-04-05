import re
import scrapy



class MusSpider(scrapy.Spider):
    name = "mus"
    allowed_domains = ["www.musinsa.com","goods.musinsa.com"]
    start_urls = ["https://www.musinsa.com/app/event/campaign/goods/1702?d_cat_cd=001&brand=&price=&color=&page=1&class_no=&list_kind=&sort=pop"]
    count = 1
    data = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        
        self.count = self.count + 1
        
        product_url = response.xpath("//div[@class='ui-goods-item__thumbnail']/a/@href").getall()
        
        for url in product_url:
            product_id = re.sub(r'\D+','',url)
            product_link =  f"https://goods.musinsa.com/api2/review/v1/view/similar-list?goodsNo={product_id}"
            yield scrapy.Request(url=product_link, headers=self.headers, callback=self.product_page)
            
        # next url
        next_page_urls = response.xpath("//div[@class='g-paging']/a").getall()
        next_page_url_count = len(next_page_urls)- 2

        if self.count <= next_page_url_count:
            updated_url = re.sub(r'page=(\d+)',f'page={self.count}',response.url)
            yield scrapy.Request(url=updated_url, headers=self.headers, callback=self.parse)
            
            
    def product_page(self, response):
        
        data = response.json()
        
        yield data
