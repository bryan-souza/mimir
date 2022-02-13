from scrapy import Spider

class QuoteSpider(Spider):
    name = "quotes"
    start_urls = ["https://www.goodreads.com/quotes/tag/programming"]
    
    def parse(self, response):
        for quote in response.css("div.quoteText"):
            
            yield {
                'text': quote.css("::text").get(),
                'author': quote.css("span.authorOrTitle::text").get()
            }

        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)