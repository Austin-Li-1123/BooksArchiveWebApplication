import requests
from bs4 import BeautifulSoup
import util.scraper_utility as utility
import scrapers.scraper as scraper

class ScraperBook(scraper.Scraper):
    '''The ScraperBook class: a web scraper for scraping Book objects'''
    def __init__(self, start_url, num_books_requested):
        super().__init__(start_url, num_books_requested)
        self.items_already_seen.append(start_url)

    def scrape_item(self):
        '''Scape the current URL and store as a Book obj
            :return A Book object containing the data scraped online'''
        req = requests.get(self.url, scraper.REQUEST_HEADER)
        soup = BeautifulSoup(req.content, 'html.parser')

        # construct Book object from soup
        book = utility.construct_book_from_soup(soup, book_url=self.url)

        # add potential book to the scraper if the requested number if not met
        if len(self.items_already_seen) < self.num_item_requested:
            # add similar books to the list future_books_list, if not seen
            for similar_book in book.similar_books:
                if similar_book not in self.items_already_seen:
                    self.future_items_list.append(similar_book)
                    self.items_already_seen.append(similar_book)

        return book
