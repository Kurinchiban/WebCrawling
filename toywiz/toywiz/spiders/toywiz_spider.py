import re
import scrapy
import random
import json
import math
import urllib.parse


class ToywizSpiderSpider(scrapy.Spider):
    name = 'toywiz_spider'
    allowed_domains = ['toywiz.com', 'tools.toywiz.com']
    start_urls = ['http://toywiz.com/']
    sub_filters = ["Character"]
    main_category = "Bandai America"
    main_domain = "https://toywiz.com"
    domin = "https://tools.toywiz.com/search/getSearch.php?"
    item_per_page = 20
    
    main_page_filter = {
        'max': 20,
        'page': 1,
        'include_filters': 'Y',
        'action': 'start',
        'callback': 'jsonCallback',
    }

    def parse(self, response):
        self.main_page_filter.update({'s': self.main_category})
        random_number = random.randint(1, 1000000000000)
        self.main_page_filter.update({'_': int(random_number)})
        url = self.generate_product_url()
        yield scrapy.Request(url=url, callback=self.parse_product_api_page)

    def generate_product_url(self):
        # NOTE:
        # Used hen the same filter key present in the payload
        # url = urllib.parse.urlencode(self.main_page_filter)
        url = ""
        for key, value in self.main_page_filter.items():
            key = key.strip()
            value = str(value)
            if isinstance(value, str):
                value = value.strip()
                value = re.sub(r'\s', '%20', value, flags=re.IGNORECASE)
            if re.findall(r'filters_\d+', key, flags=re.IGNORECASE):
                key = 'filters[]'
            url += f"{key}={value}&"
        if url[-1] == '&':
            url = url[:-1]
        product_url = self.domin + url
        return product_url

    def parse_product_api_page(self, response):
        self.main_page_filter.update({'filters_1': 'Item Type|Action Figure','filters_2': 'Company|Bandai America'})
        url = self.generate_product_url()
        filter_url = url + "&first=Y"
        yield scrapy.Request(url=filter_url, callback=self.parse_filter_page_api)
        yield scrapy.Request(url=url, callback=self.parse_sub_filter_page_api)

    def parse_sub_filter_page_api(self, response):
        data_in_json = re.sub(r'jsonCallback\(|\)', '', response.text).strip()
        data_to_dict = json.loads(data_in_json)
        filters = data_to_dict.get("filters",{})
        for key_filter,value_filter in filters.items():
            if key_filter in self.sub_filters:
                for value in value_filter:
                    self.main_page_filter.update({'g':key_filter})
                    url = self.generate_product_url
                    self.main_page_filter.update({'filters_3': f"{key_filter}|{value}"})
                    url = self.generate_product_url()
                    yield scrapy.Request(url=url, callback=self.parse_sub_filter_page_api_2,meta={"filter":key_filter,"sub_filter":value})


    def parse_sub_filter_page_api_2(self, response):

        meta = response.meta

        data_in_json = re.sub(r'jsonCallback\(|\)', '', response.text).strip()
        data_to_dict = json.loads(data_in_json)
        found_data = int(data_to_dict.get('found',''))
        current_page = int(data_to_dict.get('page',''))
        expect_pages = math.ceil(found_data/self.item_per_page)

        products = data_to_dict.get("products",[])
        for product in products:
            url = product.get('url','')
            url = self.main_domain + url
            yield scrapy.Request(url=url, callback=self.parse_product_page,meta=meta,dont_filter=True)

        if expect_pages > current_page:
            current_page = current_page + 1
            self.main_page_filter.update({'page': f"{current_page}"})
            url = self.generate_product_url()
            yield scrapy.Request(url=url, callback=self.parse_sub_filter_page_api_2,meta=meta,dont_filter=True)


    def parse_filter_page_api(self, response):

        meta = response.meta

        data_in_json = re.sub(r'jsonCallback\(|\)', '', response.text).strip()
        data_to_dict = json.loads(data_in_json)
        found_data = int(data_to_dict.get('found',''))
        current_page = int(data_to_dict.get('page','')) 
        expect_pages = math.ceil(found_data/self.item_per_page)
        
        products = data_to_dict.get("products",[])
        for product in products:
            url = product.get('url','')
            url = self.main_domain + url
            yield scrapy.Request(url=url, callback=self.parse_product_page,meta=meta)

        if expect_pages > current_page:
            current_page = current_page + 1
            self.main_page_filter.update({'page': f"{current_page}"})
            url = self.generate_product_url()
            yield scrapy.Request(url=url, callback=self.parse_filter_page_api,meta=meta)

    def parse_product_page(self,response):
        detail_data = {}
        description = response.xpath("//div[@id='itemTab1Content']/text()").getall()
        keys = response.xpath("//div[@id='itemTab2Content']/div[@class='detailLabel']")
        for key in keys:
            key_data = key.xpath(".//text()").get()
            values = key.xpath("following-sibling::a/text()").get() or key.xpath("following-sibling::text()").get()
            detail_data.update({key_data:values})
                
        guarentees = response.xpath("//div[@id='itemTab3Content']/li/text()").getall()
        visit_our_store =response.xpath("//div[@id='itemTab4Content']/text()").getall()
        product_highlights = response.xpath("//div[@class='pvDescription pvBullets productDesktop']//li/text()").getall()
        title = response.xpath("//div[@class='productTitle productDesktop']/h1/text()").get()
        price = response.xpath("//div[@class='pvPrice']/text()").get()

        yield {
            'id': response.url,
            'title': title,
            'price': price,
            'description': description,
            'guarentees': guarentees,
            'visit_our_store': visit_our_store,
            'product_highlights': product_highlights,
            'details': detail_data,
            response.meta.get('filter','') : response.meta.get('sub_filter','')
        }