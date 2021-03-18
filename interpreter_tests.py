import unittest
import interpreter.interpreter as interpreter
import util.constants as constants

class TestInterpreter(unittest.TestCase):
    '''The unit tests for the interpreter class and query classes'''
    def test_parse_no_colon(self):
        '''Test if the parser returns None and prints error if the ':' operator is missing'''
        test_input = "book.book_id"

        self.assertEqual(interpreter.parse_query(test_input), None)

    def test_parse_no_dot(self):
        '''Test if the parser returns None and prints error if the '.' operator is missing'''
        test_input = "book"

        self.assertEqual(interpreter.parse_query(test_input), None)

    def test_parse_two_dots(self):
        '''Test if the parser returns None and prints error if two '.' operators are provided'''
        test_input = "book.id.id"

        self.assertEqual(interpreter.parse_query(test_input), None)

    def test_parse_two_colons(self):
        '''Test if the parser returns None and prints error if two ':' operators are provided'''
        test_input = "book.id:id:id"

        self.assertEqual(interpreter.parse_query(test_input), None)

    def test_parse_colon_before_dot(self):
        '''Test if the parser returns None and prints error if '.' is before ':' operators'''
        test_input = "book:id.where"

        self.assertEqual(interpreter.parse_query(test_input), None)

    def test_parse_valid_input(self):
        '''Test if the parser returns the expected output with valid input'''
        test_input = "book.book_id:123"

        self.assertEqual(interpreter.parse_query(test_input), ["book", "book_id", "123"])

    def test_query_with_invalid_object_name(self):
        '''Test if the parser returns the expected output with invalid input'''
        test_input = "name.book_id:123"

        self.assertEqual(interpreter.validate_query_head(test_input), None)

    def test_query_with_close_object_name(self):
        '''Test if the parser returns the expected output with invalid input but valid name'''
        test_input = "books.book_id:123"

        self.assertEqual(interpreter.validate_query_head(test_input), None)

    def test_invalid_field_book(self):
        '''Test if the interpret knows if a random field name is wrong for books'''
        test_input = ["book", "wrong", "123"]

        self.assertEqual(interpreter.validate_field_name(test_input), False)

    def test_invalid_field_author(self):
        '''Test if the interpret knows if a random field name is wrong for authors'''
        test_input = ["author", "wrong", "123"]

        self.assertEqual(interpreter.validate_field_name(test_input), False)

    def test_valid_field_invalid_root(self):
        '''Test if the interpret rejects input when root is invalid but field is valid'''
        test_input = ["authorname", "name", "123"]

        self.assertEqual(interpreter.validate_field_name(test_input), False)

    def test_valid_field_author(self):
        '''Test if the interpret processes input when field is valid for authos'''
        test_input = ["author", "author_id", "123"]

        self.assertEqual(interpreter.validate_field_name(test_input), True)

    def test_valid_field_book(self):
        '''Test if the interpret processes input when field is valid for books'''
        test_input = ["book", "isbn", "123"]

        self.assertEqual(interpreter.validate_field_name(test_input), True)

    def test_author_field_for_book(self):
        '''Test if the interpret rejects input when field is valid for authors but root is book'''
        test_input = ["book", "author_id", "123"]

        self.assertEqual(interpreter.validate_field_name(test_input), False)

    def test_book_field_for_author(self):
        '''Test if the interpret rejects input when field is valid for books but root is author'''
        test_input = ["author", "isbn", "123"]

        self.assertEqual(interpreter.validate_field_name(test_input), False)

    def test_interpreter_extract_keyword(self):
        '''Test if the extract_keyword method correctly extarcts keyword on valid input'''
        test_keyword = "AND name1 name2"

        self.assertEqual(interpreter.extract_keyword(test_keyword, constants.AND_OPERATOR), ["name1", "name2"])

    def test_validate_keyword_valid(self):
        '''Test if the validate_keyword method returns True on valid input'''
        test_keyword = '"name"'

        self.assertEqual(interpreter.validate_keyword(test_keyword, is_comparison=False), True)

    def test_validate_keyword_invalid(self):
        '''Test if the validate_keyword method returns False on invalid input'''
        test_keyword = '"name'

        self.assertEqual(interpreter.validate_keyword(test_keyword, is_comparison=False), False)

    def test_validate_keyword_invalid_comparison(self):
        '''Test if the validate_keyword method returns False on valid input but comparison'''
        test_keyword = '"name"'

        self.assertEqual(interpreter.validate_keyword(test_keyword, is_comparison=True), False)

    def test_interpreter_no_operator(self):
        '''Test if the interpreter works when provided the basic valid input without any operator'''
        test_input = "book.isbn:123"
        itpr = interpreter.Interpreter()
        itpr.interpret_query(test_input)

        itpr.parsed_query.show_keyword_tree()
        self.assertEqual(itpr.parsed_query.root, "book")
        self.assertEqual(itpr.parsed_query.field_name, "isbn")

    def test_interpreter_no_operator_and(self):
        '''Test if the interpreter works when provided valid input with the AND operator'''
        test_input = "book.isbn:AND name1 name2"
        itpr = interpreter.Interpreter()
        itpr.interpret_query(test_input)

        itpr.parsed_query.show_keyword_tree()
        self.assertEqual(itpr.parsed_query.root, "book")
        self.assertEqual(itpr.parsed_query.field_name, "isbn")

    def test_interpreter_no_operator_or(self):
        '''Test if the interpreter works when provided valid input with the OR operator'''
        test_input = "book.isbn:OR name1 name2"
        itpr = interpreter.Interpreter()
        itpr.interpret_query(test_input)

        itpr.parsed_query.show_keyword_tree()
        self.assertEqual(itpr.parsed_query.root, "book")
        self.assertEqual(itpr.parsed_query.field_name, "isbn")

if __name__ == '__main__':
    unittest.main()
