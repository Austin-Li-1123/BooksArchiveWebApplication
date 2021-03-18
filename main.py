import sys
import argparse
import util.scraper_utility as utility
import scrapers.scraper_author as scraper_author
import data_type.book as book
import data_type.author as author
import scrapers.scraper_book as scraper_book
import util.mongo_utility as mongo_utility
import util.constants as constants

def main(argv):
    '''Main method parses the parameters, decides which mode to run in
    and execute by utilizing function from other modules
    :param argv: A list of the commandline arguments added when main.py is run'''
    # accpet and parse command line arguments
    args = parse_parameter(argv[1:])

    scrape_mode = constants.SCRAPE_MODE_KEYWORD in args
    json_create_mode = constants.CREATE_MODE_KEYWPRD in args
    json_update_mode = constants.UPDATE_MODE_KEYWPRD in args
    json_download_mode = constants.DOWNLOAD_MODE_KEYWPRD in args

    # if the program is running in scrape mode, scrape and upload to database server
    if scrape_mode:
        num_books = args.num_books[0]
        num_authors = args.num_authors[0]
        start_url = args.start_url[0]

        # Check if start_urlis valid, points to Goodreads.com, and points to a book
        is_valid_url = utility.validate_url(start_url, keyword=constants.URL_KEYWORD)
        if is_valid_url is False:
            return constants.RETURN_ON_ERROR

        # Print warning for numbers greater than 200 books and 50 authors
        if num_books > constants.WARNING_MAX_BOOK_NUM or num_authors > constants.WARNING_MAX_AUTHOR_NUM:
            print(constants.LARGE_INPUT_WARNING)

        if num_books > 2000:
            print(constants.OVERSIZE_INPUT_WARNING)
            return constants.RETURN_ON_ERROR

        # scrape content
        if num_books > 0:
            scraper = scraper_book.ScraperBook(start_url, num_books)
            utility.scrape_and_store_books(scraper, num_books)

        if num_authors > 0:
            scraper = scraper_author.ScraperAuthor(start_url, num_authors)
            utility.scrape_and_store_authors(scraper, num_authors)

    elif json_create_mode:
        json_file = args.JSON_file_create[0]
        # check if json file path is valid, correct syntax
        json_obj = utility.verify_input_json(json_file)
        if not json_obj:
            return constants.RETURN_ON_ERROR

        # create objects and upload to server
        for i in range(len(json_obj)):
            item = json_obj[i]
            if "book_url" in item:
                curr_book = book.construct_from_json(item)
                if curr_book is None:
                    print(f"EEROR: Invalid Book object provided at: {i}")
                else:
                    book_id = curr_book.insert_book_to_mongo()
                    print(f"PROGRESS: Created _id: {book_id} from JSON")

            elif "author_url" in item:
                cur_author = author.construct_from_json(item)
                if cur_author is None:
                    print(f"EEROR: Invalid Author object provided at: {i}")
                else:
                    author_id = cur_author.insert_author_to_mongo()
                    print(f"PROGRESS: Created _id: {author_id} from JSON")
            else:
                print("EEROR: Please provide json objects in the form of Books or Authors")
                return constants.RETURN_ON_ERROR

    elif json_update_mode:
        # update objects in server
        json_file = args.JSON_file_update[0]
        # check if json file path is valid, correct syntax
        json_obj = utility.verify_input_json(json_file)
        if not json_obj:
            return constants.RETURN_ON_ERROR

        for i in range(len(json_obj)):
            item = json_obj[i]
            # check if id field exists
            if "_id" not in item:
                print(f"EEROR: Object does not contain an id: {i}")
                continue

            if "book_url" in item:
                # search for this book's id on the server and update
                mongo_utility.search_and_update(item, constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_BOOK)
            elif "author_url" in item:
                mongo_utility.search_and_update(item, constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_AUTHOR)

            else:
                print("EEROR: Please provide json objects in the form of Books or Authors")
                return constants.RETURN_ON_ERROR

    elif json_download_mode:
        # open a document for writing with the given name
        file_name = utility.construct_json_filename(args.JSON_file_download[0])

        mongo_utility.download_to_json(file_name)

    return 0

def parse_parameter(argv):
    '''Parse the parameters and decide which mode to run in.
    :param argv: A list of the commandline arguments, excluding the 1st one
    :return a dict of parsed input'''

    parser = argparse.ArgumentParser(description='Decide which mode to run')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_a = subparsers.add_parser('json_create', help='a help')
    parser_a.add_argument('JSON_file_create', metavar='JSON_file_create', nargs=1,
                      help='Path of a valid JSON file. Used to create/update books and authors.')

    parser_b = subparsers.add_parser('json_update', help='a help')
    parser_b.add_argument('JSON_file_update', metavar='JSON_file_update', nargs=1,
                      help='Path of a valid JSON file. Used to create/update books and authors.')

    parser_c = subparsers.add_parser('scrape', help='scrape help')
    parser_c.add_argument('start_url', metavar='start_url', nargs=1,
                         help='The starting URL. Should be a link to a book on Goodreads.com.')
    parser_c.add_argument('num_books', metavar='num_books', type=int, nargs=1,
                         help='The number of books. Warning if value is over 200.')
    parser_c.add_argument('num_authors', metavar='num_authors', type=int, nargs=1,
                         help='The number of authors. Warning if value is over 50.')

    parser_d = subparsers.add_parser('download', help='scrape help')
    parser_d.add_argument('JSON_file_download', metavar='JSON_file_download', nargs=1,
                         help='Path of a valid JSON file. Used to create/update books and authors.')

    return parser.parse_args(argv)

if  __name__ =='__main__':
    main(sys.argv)
