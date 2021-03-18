from abc import ABC, abstractmethod
import time

REQUEST_HEADER = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

class Scraper(ABC):
    '''The Scraper class: an abstract class of web scrapers'''
    def __init__(self, start_url, num_item_requested):
        '''Construct of Scrapers
        :param start_url: The first URL to scrape
        :param num_item_requested: The total number of item needed to scrape
        '''
        self.url = start_url
        self.num_item_requested = num_item_requested
        # uses book url or author url
        self.items_already_seen = []
        #  uses book url or author url
        self.future_items_list = []

    @abstractmethod
    def scrape_item(self):
        '''Abstract method: scape the current URL and store as a obj'''

    def next_item(self):
        '''Updates the link to a book from the object's "future_book_list" and remove from there'''
        # sleep for 1.5 seconds
        time.sleep(1.5)

        if len(self.future_items_list) > 0:
            self.url = self.future_items_list.pop(0)
        else:
            # throw an error
            pass
