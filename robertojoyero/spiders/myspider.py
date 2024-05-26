import scrapy


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    # allowed_domains = ["X"]
    # start_urls = ["https://robertojoyero.com/catalogo/joyeria/?filters=product_cat%5Banillos%5D%7Ctipo%5Balianzas-compromiso%5D"]
    def start_requests(self):
        for i in range(1, 20):
            yield scrapy.Request('https://robertojoyero.com/catalogo/joyeria/page/{}/?filters=product_cat%5Banillos%5D%7Ctipo%5Balianzas-compromiso%5D'.format(i))
    def parse(self, response):
        hrefs=response.xpath('//div[@class="image_wrapper"]/a/@href').getall()
        # print(hrefs)
        # print(len(hrefs))
        for href in hrefs:
            yield scrapy.Request(href,callback=self.details)
    def details(self, response):
        url=response.url
        data={}
        image_src = response.xpath('//div[@class="woocommerce-product-gallery__image"]/a/@href').get()
        title=response.xpath('//div[@class="mcb-column-inner"]/h1/text()').get()
        price = response.xpath('//span[@class="woocommerce-Price-amount amount"]/bdi/text()').get()
        # Extract the product description
        description = response.xpath('//div[@class="woocommerce-product-details__short-description"]/text()').get()
        data['image_src'] = image_src
        data['title']=title
        data['price']=price
        data['description']=description
        ul_elements = response.xpath('//div[@class="woocommerce-product-details__short-description"]/ul/li')
        for li in ul_elements:
            label = li.xpath('./b/text()').get().strip(':')
            value = li.xpath('./text()').get().strip()
            data[label] = value
        data['url']=url
        yield  data