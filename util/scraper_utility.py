import re
import json
import PySimpleGUI as sg
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import data_type.book
import data_type.author
import util.constants as constants

def validate_url(start_url, keyword):
    '''Check if start_urlis valid, points to Goodreads.com, and points to a book
        :param start_url: The URL to be checked
        :param keyword: The keyword that the URL must contain'''
    # check if start_urlis valid
    val = URLValidator()
    try:
        val(start_url)
    except ValidationError:
        print("Invalid URL.")
        return False

    # check if start_url points to Goodreads.com, and points to a book
    if keyword not in start_url:
        print("URL does not point to a book on Goodreads.com")
        return False
    return True

def construct_book_from_soup(soup, book_url):
    '''construct Book object from soup
        :param soup: The soup object obtained from scraper
        :param book_url: The URL of the book page
        :return A valid Book object'''
    book_title = format_book_title(soup.find(id="bookTitle").get_text())

    book_id = get_id_from_url(book_url)

    book_isbm = soup.find("span", itemprop="isbn").get_text() if soup.find("span", itemprop="isbn") else print_error_message("ISBN is not avaiable", book_url)

    author_anchor = soup.find_all(class_="authorName")[0]

    author_url = author_anchor.get('href')

    author_name = author_anchor.get_text()

    rating = float(soup.find("span", itemprop="ratingValue").get_text())

    rating_count_string = soup.find("meta", itemprop="ratingCount").get_text()
    rating_count = int(re.sub('[^0-9,]', "", rating_count_string).replace(",", ""))

    review_count_string = soup.find("meta", itemprop="reviewCount").get_text()
    review_count = int(re.sub('[^0-9,]', "", review_count_string).replace(",", ""))

    image_url = soup.find(id="coverImage").get('src') if soup.find(id="coverImage")  else print_error_message("Cover image is not avaiable", book_url)

    similar_books_li = soup.find_all("li", class_="cover")
    similar_books = []
    for list_item in similar_books_li:
        similar_books.append(list_item.a.get('href'))

    # construct the book object
    new_book = book.Book(book_url, book_title, book_id, book_isbm, author_url, author_name, rating, rating_count, review_count, image_url, similar_books)

    return new_book

def get_id_from_url(url):
    '''extract the number after: https://www.goodreads.com/book/show/ + 3735293 + -clean-code
        :param url: The url to get the id from
        :return any id able to obtain from the given url'''

    ints_in_url = re.findall(r'\d+', url)
    return int(ints_in_url[0])


def format_book_title(raw_title):
    '''Some titles contain '\n's. This function removes them
        :param raw_title: the original title, contains useless charactors
        :return a clean version of the title'''

    extracted_title = raw_title.replace("\n", "")
    # remove space charactors in the head and tail of title
    while extracted_title[0] == ' ':
        extracted_title = extracted_title[1:]
    while extracted_title[-1] == ' ':
        extracted_title = extracted_title[:-1]

    return extracted_title


def construct_author_from_soup(soup, author_url, related_authors):
    '''construct Author object from soup
        :param soup: The soup object obtained from scraper
        :param author_url: The URL of the author page
        :return A valid Author object'''
    author_name = soup.find("span", itemprop="name").get_text()

    author_id = get_id_from_url(author_url)

    rating = float(soup.find("span", itemprop="ratingValue").get_text())

    rating_count_string = soup.find("span", itemprop="ratingCount").get_text()
    rating_count = int(re.sub('[^0-9,]', "", rating_count_string).replace(",", ""))

    review_count_string = soup.find("span", itemprop="reviewCount").get_text()
    review_count = int(re.sub('[^0-9,]', "", review_count_string).replace(",", ""))

    image_url = soup.find("img", itemprop="image").get('src') if soup.find("img", itemprop="image") else print_error_message("cover image is not avaiable", author_url)

    # extract the book urls from book table
    author_books_raw = soup.find("table", class_="stacked tableList").find_all("a", class_="bookTitle")
    author_books = []
    for book_link_anchor in author_books_raw:
        author_books.append(constants.URL_ROOT + book_link_anchor.get('href'))

    # construct the book object
    new_author = author.Author(author_name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books)

    return new_author

def print_error_message(error_message, url):
    '''print the provided error message in obtaining an url
        :param error_message: a string of the actual message
        :param url: the url where the error take place
        :return a compposed error message'''
    print(f"ERROR: {error_message} at {url}")
    return error_message

def verify_input_json(json_file):
    '''check if json file path is valid, correct syntax
        :param json_file: name of the json file
        :return a valid json file name'''
    try:
        opened_file = open(json_file)
    except OSError:
        print("ERROR: Not a valid file")
        return None
    try:
        return json.load(opened_file)
    except ValueError:
        print("ERROR: Invalid JSON file")
        return None

def construct_json_filename(original_name):
    '''fix the name of the json file as download destination if the given one is not valid
        :param original_name: user-provided name of the json file
        :return a valid name of the json file'''

    default_name = "data_dataload.JSON"
    # check if the name ends with .JSON
    if original_name[-5:] != ".JSON":
        print("ERROR: Invalid JSON file name, using: "+ {default_name})
        return default_name
    return original_name

def scrape_and_store_books(book_scraper, num_books):
    '''Scrape the books of the amount num_books and store them individually
    right after scraping, instead of all together.
    :param scraper_book: The ScraperBook object. Capable of scraping books
    :param num_books: number of books indicated by the user.'''

    sg.one_line_progress_meter('Scraping and storing books!', 0,num_books, '-key-')
    for i in range(num_books):
        # scrape and upload current book to mongo
        scraped_book = book_scraper.scrape_item()
        scraped_book.insert_book_to_mongo()
        if i != (num_books - 1):
            # update the book url
            book_scraper.next_item()
        del scraped_book
        sg.one_line_progress_meter('Scraping and storing books!', i+1,num_books, '-key-')

def scrape_and_store_authors(author_scraper, num_authors):
    '''Scrape the authors of the amount num_authors and store them individually
    right after scraping, instead of all together.
    :param scraper_author: The ScraperAuthor object. Capable of scraping authors.
    :param num_authors: number of authors indicated by the user.'''

    sg.one_line_progress_meter('Scraping and storing authors!', 0,num_authors, '-key-')
    for i in range(num_authors):
        # scrape and upload current book to mongo
        scraped_author = author_scraper.scrape_item()
        scraped_author.insert_author_to_mongo()
        if i != (num_authors - 1):
            # update the book url
            author_scraper.next_item()
        del scraped_author
        sg.one_line_progress_meter('Scraping and storing authors!', i+1,num_authors, '-key-')
