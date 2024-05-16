import scrapy

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "mongo/authors.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']


    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            author_link = quote.xpath("span/a/@href").extract()[0]
            yield response.follow(author_link, self.parse_author)

        next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        for author in response.xpath("//div[@class='author-details']"):
            yield {
                    'fullname': author.xpath("//h3[@class='author-title']/text()").extract(),
                    'born_date': author.xpath("//p/span[@class='author-born-date']/text()").extract(),
                    'born_location': author.xpath("//p/span[@class='author-born-location']/text()").extract(),
                    'description': author.xpath("//div[@class='author-description']/text()").extract()[0].strip(),
                }