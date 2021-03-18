import pymongo

# main and mongo macros
WARNING_MAX_BOOK_NUM = 200
WARNING_MAX_AUTHOR_NUM = 50
RETURN_ON_ERROR = 1
URL_KEYWORD = "goodreads.com/book/show/"
BOOK_URL_HEAD = "https://www.goodreads.com/book/show/"
URL_ROOT = "https://www.goodreads.com"
DATABASE_NAME_TEST = "test-1"
DATABASE_NAME_MAIN = "sp21-cs242-assignment"
COLLECTION_NAME_BOOK = "Books"
COLLECTION_NAME_AUTHOR = "Authors"
NOT_AVAILABLE_MESSAGE = "Not available"
ENV_FILENAME = "client_password.txt"
CLIENT_PASSCODE = open(ENV_FILENAME, "r").read()
MONGO_CLIENT_LINK_HEAD = "mongodb+srv://"+ CLIENT_PASSCODE +"@cluster0.k6d5c.mongodb.net/"
MONGO_CLIENT_LINK = MONGO_CLIENT_LINK_HEAD + "CS242-SP21-ASSIGNMENT2.0?retryWrites=true&w=majority"
MONGO_CLIENT = pymongo.MongoClient(MONGO_CLIENT_LINK)

LARGE_INPUT_WARNING = "Warning: scraping more than 200 books or 50 authors."
OVERSIZE_INPUT_WARNING = "Warning: No scraping over 2000 books."

SCRAPE_MODE_KEYWORD = "num_books"
CREATE_MODE_KEYWPRD = "JSON_file_create"
UPDATE_MODE_KEYWPRD = "JSON_file_create"
DOWNLOAD_MODE_KEYWPRD = "JSON_file_download"

# interpreter macros
FIELD_OPERATOR = '.'
CONTAINS_OPERATOR = ':'
EXACT_OPERATOR = '"'
AND_OPERATOR = "AND"
OR_OPERATOR = "OR"
NOT_OPERATOR = "NOT"
GRAETER_OPERATOR = ">"
SMALLER_OPERATOR = "<"
WILD_OPERATOR = "*"
FIELD_COUNT = 2

VALID_HEADS = ["book", "author"]
ROOT_ERROR_MESSAGE = "ERROR: Root of qury is not a known type."
FIELD_ERROR_MESSAGE = "ERROR: The field does not exist."
SYNTAX_ERROR_MESSAGE = "ERROR: The qury does not have correct syntax."
KEYWORD_NONEXIST_MESSAGE = "ERROR: The qury does not have any keyword."
KEYWORD_MISFORMAT_MESSAGE = "ERROR: The keyword does not have the correct format."

# flask server constants
ID_LENGTH = 24
ID_LENGTH_ERROR = "ERROR: The provided ID is not of the correct length."
ID_NOT_EXIST_ERR = "ERROR: The provided ID does not exist."
DELETE_DONE_MESSAGE = "Delete has been successful"

# STATUSCODE_SUCCESS = 204 # success, no response
STATUSCODE_SUCCESS = 200
STATUSCODE_BAD_REQUEST = 400
STATUSCODE_NOT_FOUND = 404
METHOD_NAME = "GET"

# command line gui
GET_BOOK = "get_book"
GET_AUTHOR = "get_author"
GET_SEARCH = "get_search"

PUT_BOOK = "put_book"
PUT_AUTHOR = "put_author"

POST_BOOK = 'post_book'
POST_BOOKS ='post_books'
POST_AUTHOR ='post_author'
POST_AUTHORS = 'post_authors'
POST_SEARCH = 'post_search'

DELETE_BOOK = "delete_book"
DELETE_AUTHOR = "delete_author"

END_NODE_NAME = "end"
EVENT_TAG_NAME = "event"
