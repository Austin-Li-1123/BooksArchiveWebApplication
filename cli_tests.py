import unittest
import util.scraper_utility as utility
import main
import util.constants as constants

class TestCommandLineInterface(unittest.TestCase):
    '''The unit tests for the command line interface and scraper classes'''
    def test_argument_parsing(self):
        '''Test if the parser correctly parses the valid input parameters'''
        test_url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        argv, test_num_books, test_num_authors = generate_commandline_parameters(test_url)
        args = main.parse_parameter(argv)

        self.assertEqual(args.start_url[0], test_url)
        self.assertEqual(str(args.num_books[0]), test_num_books)
        self.assertEqual(str(args.num_authors[0]), test_num_authors)

    def test_invalid_url_one(self):
        '''Test if invalid URLs are rejected'''
        test_url = 'rklwdkslfkes'
        argv, _, _ = generate_commandline_parameters(test_url)
        args = main.parse_parameter(argv)

        is_valid_url = utility.validate_url(args.start_url[0], keyword=constants.URL_KEYWORD)

        self.assertEqual(is_valid_url, False)

    def test_invalid_url_two(self):
        '''Test if URLs that does not point to Goodreads.com are rejected'''
        test_url = 'http://www.google.com'
        argv, _, _ = generate_commandline_parameters(test_url)
        args = main.parse_parameter(argv)

        is_valid_url = utility.validate_url(args.start_url[0], keyword=constants.URL_KEYWORD)

        self.assertEqual(is_valid_url, False)

    def test_invalid_url_three(self):
        '''Test if URLs that does not point to a book on Goodreads.com are rejected'''
        test_url = 'https://www.goodreads.com/?ref=nav_home'
        argv, _, _ = generate_commandline_parameters(test_url)
        args = main.parse_parameter(argv)

        is_valid_url = utility.validate_url(args.start_url[0], keyword=constants.URL_KEYWORD)

        self.assertEqual(is_valid_url, False)

    def test_get_book_id_from_url(self):
        '''Test if get_bookID_from_url successfully extract the number from URLs'''
        test_url_one = 'https://www.goodreads.com/book/show/3735293-clean-code'
        test_url_two = 'https://www.goodreads.com/book/show/6953508-some-we-love-some-we-hate-some-we-eat'
        test_url_three = 'https://www.goodreads.com/book/show/51714.The_Sexual_Politics_of_Meat'

        self.assertEqual(utility.get_id_from_url(test_url_one), 3735293)
        self.assertEqual(utility.get_id_from_url(test_url_two), 6953508)
        self.assertEqual(utility.get_id_from_url(test_url_three), 51714)

    def test_invalid_input_json(self):
        '''Test if the verify_input_json function returns none for invalid json files'''
        invalid_json_name = "names.txt"
        self.assertEqual(utility.verify_input_json(invalid_json_name), None)

    def test_valid_input_json(self):
        '''Test if the verify_input_json function returns none for invalid json files proper json files tha tdo not exist'''
        valid_json_name = "names.JSON"
        self.assertEqual(utility.verify_input_json(valid_json_name), None)

def generate_commandline_parameters(test_url):
    '''Helper function for constructing test commandline inputs
        :param test_url: The URL field in the commandline inputs
    '''
    test_num_books = '2'
    test_num_authors = '30'
    argv = ["scrape", test_url, test_num_books, test_num_authors]

    return argv, test_num_books, test_num_authors

if __name__ == '__main__':
    unittest.main()
