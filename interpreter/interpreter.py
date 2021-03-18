import util.constants as constants
import data_type.book as book
import data_type.author as author
import interpreter.query_class as query_class

class Interpreter:
    '''The Interpreter class. Capable of interpreting commands in defined formats'''
    def __init__(self):
        self.input_string = None
        self.parsed_query = None

    def interpret_query(self, query_string):
        '''Parse the query and store it in a tree. The method to call out side of class
            :param query_string: the raw input string of query'''
        # parse the query into object.field:content
        self.input_string = query_string
        parsed_substrings = parse_query(self.input_string)

        # object field must be a valid object type
        object_type = validate_query_head(parsed_substrings[0])

        # Print error or continue parsing [0,1] for [book, author]
        if object_type is None:
            print(constants.ROOT_ERROR_MESSAGE)
            return

        # check if field exists
        is_valid_field = validate_field_name(parsed_substrings)
        if not is_valid_field:
            print(constants.FIELD_ERROR_MESSAGE)
            return

        if len(parsed_substrings[2]) == 0:
            print(constants.KEYWORD_NONEXIST_MESSAGE)
            return

        self.parsed_query = query_class.Query(parsed_substrings[0], parsed_substrings[1])

        # parse the query content
        self.parse_keyword(parsed_substrings[2])

    def parse_keyword(self, query_string):
        '''Parse the keyword portion of the original raw input query string
            :param query_string: the content of the query.'''
        if len(query_string) == 0:
            return
        # AND operator
        if constants.AND_OPERATOR == query_string[:len(constants.AND_OPERATOR)]:
            keyword_list = extract_keyword(query_string, constants.AND_OPERATOR)
            # check if a keyword exist
            if keyword_list is None:
                return

            # validate keywords
            for keyword in keyword_list:
                if not validate_keyword(keyword, is_comparison=False):
                    return

            # insert to tree
            self.parsed_query.insert_tree_single(constants.AND_OPERATOR)
            self.parsed_query.insert_tree_pair(keyword_list, 0)

        # OR operator
        elif constants.OR_OPERATOR == query_string[:len(constants.OR_OPERATOR)]:
            keyword_list = extract_keyword(query_string, constants.OR_OPERATOR)
            # check if a keyword exist
            if keyword_list is None:
                return

            # validate keywords
            for keyword in keyword_list:
                if not validate_keyword(keyword, is_comparison=False):
                    return

            # insert to tree
            self.parsed_query.insert_tree_single(constants.OR_OPERATOR)
            self.parsed_query.insert_tree_pair(keyword_list, 0)

        # NOT operator
        elif constants.NOT_OPERATOR == query_string[:len(constants.NOT_OPERATOR)]:
            keyword = extract_keyword(query_string, constants.NOT_OPERATOR)
            # check if a keyword exist
            if keyword is None or not validate_keyword(keyword, is_comparison=False):
                return

            # insert to tree
            self.parsed_query.insert_tree_single(constants.NOT_OPERATOR)
            self.parsed_query.insert_tree_single(keyword)

        # > operator
        elif constants.GRAETER_OPERATOR == query_string[:len(constants.GRAETER_OPERATOR)]:
            keyword = extract_keyword(query_string, constants.GRAETER_OPERATOR)
            # check if a keyword exist
            if keyword is None or not validate_keyword(keyword, is_comparison=True):
                return

            # insert to tree
            self.parsed_query.insert_tree_single(constants.GRAETER_OPERATOR)
            self.parsed_query.insert_tree_single(keyword)

        # < operator
        elif constants.SMALLER_OPERATOR == query_string[:len(constants.SMALLER_OPERATOR)]:
            keyword = extract_keyword(query_string, constants.SMALLER_OPERATOR)
            # check if a keyword exist
            if keyword is None or not validate_keyword(keyword, is_comparison=True):
                return

            # insert to tree
            self.parsed_query.insert_tree_single(constants.SMALLER_OPERATOR)
            self.parsed_query.insert_tree_single(keyword)

        # keyword itself
        else:
            self.parsed_query.insert_tree_single(query_string)

def validate_keyword(keyword, is_comparison):
    '''Check if the keyword contains "". If it does, the format has to be correct.
     "" also can not be used with >, <
        :param keyword: the keyword portion of query string.
        :param is_comparison: true for >,<. false otherwise
        :return a boolean, indicating if the keyword is valid'''
    if '"' in keyword:
        if is_comparison:
            return False

        if keyword[0] == '"' and keyword[-1] == '"':
            print(constants.KEYWORD_MISFORMAT_MESSAGE)
            return True

        return False

    # return true if the string does not contain quotation marks
    return True

def extract_keyword(query_string, operator):
    '''Extract the key word, remove the operator
        :param query_string: the keyword portion of query string.
        :param operator: A string of operator
        :return A list of string, None on error. None on error'''
    operator_string = operator + " "
    if query_string[:len(operator_string)] == operator_string:
        # in case operator requires 2 arguments
        if operator == constants.AND_OPERATOR or operator == constants.OR_OPERATOR:
            keyword_list = query_string[len(operator_string):].split(" ")
            if len(keyword_list) != 2:
                return None
            else:
                return keyword_list
        else:
            return query_string[len(operator_string):]

    return None

def validate_query_head(query_string):
    '''Compare the head of the query to the valid head. Valid if matches.
        :param query_string: the keyword portion of query string.
        :return [0,1] for [book, author]. None if invalid'''
    for i in range(len(constants.VALID_HEADS)):
        if constants.VALID_HEADS[i] == query_string:
            return i
    return None

def parse_query(query_string):
    '''Parse the given query into substrings based on the delimiters
        :param query_string: the keyword portion of query string.
        :return list of parsed substrings. None if invalid'''
    parsed_substrings = []
    # parse field operator, should only be 2 parts
    prased_field_list = query_string.split(constants.FIELD_OPERATOR)
    if len(prased_field_list) != constants.FIELD_COUNT:
        # syntax error
        print(constants.SYNTAX_ERROR_MESSAGE)
        return None

    parsed_substrings.append(prased_field_list[0])

    # parse the right side of '.'
    prased_content_list = prased_field_list[1].split(constants.CONTAINS_OPERATOR)
    if len(prased_content_list) != constants.FIELD_COUNT:
        # syntax error
        print(constants.SYNTAX_ERROR_MESSAGE)
        return None

    parsed_substrings.append(prased_content_list[0])
    parsed_substrings.append(prased_content_list[1])

    return parsed_substrings

def validate_field_name(parsed_substrings):
    '''Check if field exists for the given object type
        :param parsed_substrings: a list in the form [object, field, content]
        :return boolean, true if field is valid'''
    # if obj is book
    if parsed_substrings[0] == constants.VALID_HEADS[0]:
        if parsed_substrings[1] in book.fields:
            return True

    elif parsed_substrings[0] == constants.VALID_HEADS[1]:
        # obj is author
        if parsed_substrings[1] in author.fields:
            return True

    return False
