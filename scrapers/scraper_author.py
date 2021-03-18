import requests
from bs4 import BeautifulSoup
import util.scraper_utility as utility
import scrapers.scraper as scraper

class ScraperAuthor(scraper.Scraper):
    '''The ScraperAuthor class: a web scraper for scraping Author objects'''
    def __init__(self, start_url, num_authors_requested):
        '''Construct of Scrapers
        :param start_url: The first URL to scrape
        :param num_authors_requested: The total number of Authors needed to scrape
        '''
        super().__init__(start_url, num_authors_requested)

        self.url = self.get_author_link_from_book_link()
        self.items_already_seen.append(start_url)

    def scrape_item(self):
        '''Scape the current URL and store as an Author obj
            :return An Author object containing the data scraped online'''
        req = requests.get(self.url, scraper.REQUEST_HEADER)
        soup = BeautifulSoup(req.content, 'html.parser')

        related_authors = self.get_related_authors()
        # construct Book object from soup
        author = utility.construct_author_from_soup(soup, author_url=self.url, related_authors=related_authors)

        # add potential authors to the scraper if the requested number if not met
        if len(self.items_already_seen) < self.num_item_requested:
            # add similar authors to the list future_books_list, if not seen
            for related_author in author.related_authors:
                if related_author not in self.items_already_seen:
                    self.future_items_list.append(related_author)
                    self.items_already_seen.append(related_author)

        return author

    def get_author_link_from_book_link(self):
        '''Called when the object is initialized.
            :return An URL pointing to the author of the book URL provided'''
        req = requests.get(self.url, scraper.REQUEST_HEADER)
        soup = BeautifulSoup(req.content, 'html.parser')

        return soup.find_all(class_="authorName")[0].get('href')

    def get_related_authors(self):
        '''Go the the related authors page and scrape the author names
            :return A list of author URLs'''
        related_authors_url = self.url.replace("show", "similar")

        req = requests.get(related_authors_url, scraper.REQUEST_HEADER)
        soup_similar_author = BeautifulSoup(req.content, 'html.parser')

        related_authors_raw = soup_similar_author.find_all("a", itemprop="url", class_="gr-h3")
        related_authors = []
        for author_span in related_authors_raw:
            related_authors.append(author_span.get('href'))

        # first entry is alway is the person themselves
        return related_authors[1:]
