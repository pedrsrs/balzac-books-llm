import re
import scrapy
from scrapy.crawler import CrawlerProcess

AUTHOR_NAME = "Honoré de Balzac"
#BOOKS_DIRECTORY = "/books"

class GutenbergScraper(scrapy.Spider):
    name = 'gutenberg_scraper'
    start_urls = ['https://www.gutenberg.org/ebooks/author/251']
    book_links = {}

    def parse(self, response):
        items = response.css('li.booklink')

        for book in items:
            title = book.css('span.title::text').get()
            author = book.css('span.subtitle::text').get()
            link = book.css('a.link::attr(href)').get()
            
            book_id_pattern = r"/ebooks/(\d+)"
            id_match = re.search(book_id_pattern, link)

            if id_match and author and self.verify_author(author) and not self.verify_different_translations(title):
                
                book_id = id_match.group(1)
                book_link = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
                self.book_links[book_link] = title

            next_page_link = response.css('a[title="Go to the next page of results."]::attr(href)').extract_first()
            next_page_link = "https://www.gutenberg.org"+next_page_link

            if next_page_link:
                yield scrapy.Request(url=next_page_link, callback=self.parse)

        yield from self.parse_links()

    def parse_links(self):
        for link, title in self.book_links.items():
            yield scrapy.Request(url=link, callback=self.save_book_content, cb_kwargs={'title': title})

    def save_book_content(self, response, title):
        title = title.lower().replace(" ", "_")

        filename = f"{title}.txt"

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)

    def verify_different_translations(self, title):
        pattern = r'\([A-Za-z]+\)'
        return bool(re.search(pattern, title))

    def verify_author(self, author):
        return AUTHOR_NAME in author

process = CrawlerProcess()
process.crawl(GutenbergScraper)
process.start()
