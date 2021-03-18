import json
import util.mongo_utility
import util.constants

fields = ["book_url", "title", "book_id", "isbn", "author_url", "author", "rating", "rating_count", "review_count", "image_url", "similar_books"]

class Book:
    '''The Book class. Objects contain information of books'''
    def __init__(self, book_url, title, book_id, isbn, author_url, author, rating, rating_count, review_count, image_url, similar_books):
        '''Initialize an Author obj from the data of its fields
            :param book_url: URL of the Book
            :param title: Name of the Book
            :param book_id: A unique identifier of the book
            :param isbn: The ISBN of the book
            :param author_url: URL of the author of the book
            :param author: Author of the book
            :param rating: The rating of the book
            :param rating_count: The number of rating the book received
            :param review_count: The number of comments the book received
            :param image_url: A URL of the book's image
            :param similar_books: A list of books similar or related to the book
            :return a new Book object'''
        self.book_url = book_url
        self.title = title
        self.book_id = book_id
        self.isbn = isbn
        self.author_url = author_url
        self.author = author
        self.rating = rating
        self.rating_count = rating_count
        self.review_count = review_count
        self.image_url = image_url
        self.similar_books = similar_books

    def print_book(self):
        '''Print the JSON form of the Book's fields'''
        print(self.construct_json())

    def construct_json(self):
        '''Construct the JSON form of the Book's fields
        :return a JSON form of the object's fields'''
        json_string = json.dumps(self.__dict__)
        return json_string

    def insert_book_to_mongo(self):
        '''Insert the json form(dict) to the mongodb server
        :return the id of the inserted object'''
        return mongo_utility.insert_json_to_mongo(self.__dict__, constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_BOOK)

def construct_from_json(json_obj):
    '''construct a Book object from a json object
        :return None if json is invalid, a Book object if otherwise'''
    book = Book(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    for field in book.__dict__.keys():
        if field in json_obj:
            book.__dict__[field] = json_obj[field]
        else:
            return None
    return book
