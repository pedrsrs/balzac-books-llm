import re
import scrapy
from scrapy.crawler import CrawlerProcess

AUTHOR_NAME = "Honoré de Balzac"

class GutenbergScraper(scrapy.Spider):
    name = 'gutenberg_scraper'
    start_urls = ['https://www.gutenberg.org/ebooks/author/251']

    def parse(self, response):
        item_links = response.css('li.booklink')

        for book in item_links:
            title = book.css('span.title::text').get()
            author = book.css('span.subtitle::text').get()
            link = book.css('a.link::attr(href)').get()
            link = 'https://www.gutenberg.org'+link

            if self.verify_different_translations(title) is False and self.verify_author(author) is True:
                yield {
                    'title': title,
                    'author': author,
                    'link': link
                }

        next_page_link = response.css('a[title="Go to the next page of results."]::attr(href)').extract_first()
        next_page_link = "https://www.gutenberg.org"+next_page_link
        if next_page_link:
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def verify_different_translations(self, title):    
        pattern = r'\([A-Za-z]+\)'
        return bool(re.search(pattern, title))
    
    def verify_author(self, author):
        return AUTHOR_NAME in author

process = CrawlerProcess()
process.crawl(GutenbergScraper)
process.start()
