"""crawl the quotes in website
"""
import scrapy
from ..items import MycrawlerItem


class QuotesSpider(scrapy.Spider):
    """Quotes Spider"""
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        items = MycrawlerItem()
        quotes = response.css("div.quote")
        for quote in quotes:
            items["text"] = quote.css("span.text::text").get()[1:-1]
            items["author"] = quote.css("small.author::text").get()
            items["tags"] = quote.css("div.tags>a.tag::text").getall()
            yield items
        next_page = response.css("li.next>a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
