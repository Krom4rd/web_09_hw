import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "mongo/quotes.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath("//div[@class = 'quote']")
        for quote in quotes:
            yield {'tags': quote.xpath(".//a[@class='tag']/text()").extract(),
                   'author': quote.xpath(".//small[@class='author']/text()").get(),
                   'quote': quote.xpath(".//span[@class='text']/text()").get()
                   }
            
        yield from self.next_page(response)

    def next_page(self, response):
        next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)
            