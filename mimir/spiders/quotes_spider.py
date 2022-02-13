from scrapy import Spider
from rich import print

class QuoteSpider(Spider):
    name = "quotes"
    start_urls = ["https://www.goodreads.com/quotes/tag/programming"]
    
    def parse(self, response):
        for quote in response.css("div.quoteText"):
            
            yield {
                'text': quote.css("::text").get(),
                'author': quote.css("span.authorOrTitle::text").get()
            }