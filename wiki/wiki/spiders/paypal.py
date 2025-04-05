import scrapy

class PaypalSpider(scrapy.Spider):
    name = "paypal"
    allowed_domains = ["https://en.wikipedia.org/"]
    start_urls = ["https://en.wikipedia.org/wiki/PayPal"]

    def parse(self, response):
        
        about = {}
        history = response.xpath('//figure[@class="mw-default-size"]/following::p/text()').getall()
        # company_data = response.xpath('//table[@class="infobox ib-company vcard"]/descendant::tr')
        
        # for data in company_data:
        #     key_xpath = "./th[@class='infobox-label']/text()"
        #     value_xpath = "./td[@class='infobox-data']//text()"
            
        #     if not data.xpath(key_xpath):
        #         key_xpath = "./th[@class='infobox-data']//a//text()"
            
        #     if not data.xpath(value_xpath):
        #         value_xpath = "./td[@class='infobox-data']//a//text()"
            
        #     if data.xpath(key_xpath) and data.xpath(value_xpath):
        #         key = data.xpath(key_xpath).get()
        #         value = data.xpath(value_xpath).getall()
        #         about.update({key: value})
                
        data = {
            "History" : history,
            # "About": about
        }
        return data