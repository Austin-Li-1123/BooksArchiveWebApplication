import json
import util.mongo_utility
import util.constants

fields = ["name", "author_url", "author_id", "rating", "rating_count", "review_count", "image_url", "related_authors", "author_books"]

class Author:
    '''The Author class. Objects contain information of authors'''
    def __init__(self, name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books):
        '''Initialize an Author obj from the data of its fields
            :param name: Name of the Author
            :param author_url: The page URL
            :param author_id: A unique identifier of the author
            :param rating: The rating of the author
            :param rating_count: The number of rating the author received
            :param review_count: The number of comments the author received
            :param image_url: A URL of the Author's image
            :param related_authors: A list of Author related to the author
            :param author_books: A list of books by the author
            :return a new Author object'''
        self.name = name
        self.author_url = author_url
        self.author_id = author_id
        self.rating = rating
        self.rating_count = rating_count
        self.review_count = review_count
        self.image_url = image_url
        self.related_authors = related_authors
        self.author_books = author_books

    def print_author(self):
        '''Print the JSON form of the Author's fields'''
        print(self.construct_json())

    def construct_json(self):
        '''Construct the JSON form of the Author's fields
        :return a JSON form of the object's fields'''
        json_string = json.dumps(self.__dict__)
        return json_string

    def insert_author_to_mongo(self):
        '''Insert the json form(dict) to the mongodb server
        :return the id of the inserted object'''
        return mongo_utility.insert_json_to_mongo(self.__dict__, constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_AUTHOR)

def construct_from_json(json_obj):
    '''construct an Author object from a json object
        :return None if json is invalid, an Author object if otherwise'''
    author = Author(0, 0, 0, 0, 0, 0, 0, 0, 0)
    for field in author.__dict__.keys():
        if field in json_obj:
            author.__dict__[field] = json_obj[field]
        else:
            return None
    return author
