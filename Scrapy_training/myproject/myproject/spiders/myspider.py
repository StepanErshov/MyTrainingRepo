import scrapy

class MySpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["job.mts.ru"]
    start_urls = ["https://job.mts.ru/programs/start#start-page-internship-list"]

    def parse(self, response):
        title = response.css("h1::text").get()
        
        description = response.xpath("//p[@class='desc']/text()").get()
        
        links = response.css("a::attr(href)").getall()
        
        yield {
            "title": title,
            "description": description,
            "links": links,
        }

class JSSpider(scrapy.Spider):
    name = "jsspider"
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://docs.scrapy.org",
            meta={"playwright": True},
        )

    def parse(self, response):
        yield {"title": response.css("h1::text").get(),
               "description": response.xpath("//p[@class='desc']/text()").get(),
               "links": response.css("a::attr(href)\n").getall()}