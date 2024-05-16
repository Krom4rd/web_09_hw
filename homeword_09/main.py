from my_scrap.my_scrap.spiders import authors, quotes
from scrapy.crawler import CrawlerProcess

if __name__=="__main__":

# run spider
    result = CrawlerProcess()
    result.crawl(authors.AuthorsSpider)
    result.crawl(quotes.QuotesSpider)
    result.start()
