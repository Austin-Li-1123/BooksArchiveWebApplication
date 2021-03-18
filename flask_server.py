import flask
from flask import Flask, request, jsonify, after_this_request
import util.mongo_utility as mongo_utility
import util.scraper_utility as utility
import util.constants as constants
import main

app = Flask(__name__)

@app.route('/api/get/book', methods=[constants.METHOD_NAME])
def get_book():
    '''Get a book based on the id provided. Search the MAIN database for a match and return
        :return a json string if the id is valid, a repsonse containing an error message
        and a status code otherwise.'''
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    input_keys = list(flask.request.args.to_dict().keys())
    if len(input_keys) != 1 or input_keys[0] != "id":
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    id_value = str(flask.request.args.get('id', None))
    # check if 12 is of the right length
    if len(id_value) != constants.ID_LENGTH:
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    json_data = mongo_utility.search_with_id(constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_BOOK, id_value)
    if json_data is None:
        return flask.Response(constants.ID_NOT_EXIST_ERR, status=constants.STATUSCODE_NOT_FOUND)

    # convert id field to string
    json_data["_id"] = str(json_data["_id"])
    return flask.jsonify(json_data), constants.STATUSCODE_SUCCESS


@app.route('/api/get/author', methods=[constants.METHOD_NAME])
def get_author():
    '''Get a author based on the id provided. Search the MAIN database for a match and return
        :return a json string if the id is valid, a repsonse containing an error message
        and a status code otherwise.'''
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # check if no other parameters are used. only id
    input_keys = list(flask.request.args.to_dict().keys())
    if len(input_keys) != 1 or input_keys[0] != "id":
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    id_value = str(flask.request.args.get('id', None))
    # check if 12 is of the right length
    if len(id_value) != constants.ID_LENGTH:
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    json_data = mongo_utility.search_with_id(constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_AUTHOR, id_value)
    if json_data is None:
        return flask.Response(constants.ID_NOT_EXIST_ERR, status=constants.STATUSCODE_NOT_FOUND)

    # convert id field to string
    json_data["_id"] = str(json_data["_id"])
    return flask.jsonify(json_data), constants.STATUSCODE_SUCCESS

    return jsonify(jsonResp)

@app.route('/api/delete/book', methods=[constants.METHOD_NAME])
def delete_book():
    '''Delete a book based on the id provided. Search the MAIN database for a match and return
        :return a response with 200 if the id is valid, a repsonse containing an error message
        and a status code otherwise.'''
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # check if no other parameters are used. only id
    input_keys = list(flask.request.args.to_dict().keys())
    if len(input_keys) != 1 or input_keys[0] != "id":
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    id_value = str(flask.request.args.get('id', None))
    # check if 12 is of the right length
    if len(id_value) != constants.ID_LENGTH:
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    mongo_utility.delete_with_id(constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_BOOK, id_value)

    return flask.Response(constants.DELETE_DONE_MESSAGE, status=constants.STATUSCODE_SUCCESS)

@app.route('/api/delete/author', methods=[constants.METHOD_NAME])
def delete_author():
    '''Delete an author based on the id provided. Search the MAIN database for a match and return
        :return a response with 200 if the id is valid, a repsonse containing an error message
        and a status code otherwise.'''
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # check if no other parameters are used. only id
    input_keys = list(flask.request.args.to_dict().keys())
    if len(input_keys) != 1 or input_keys[0] != "id":
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    id_value = str(flask.request.args.get('id', None))
    # check if 12 is of the right length
    if len(id_value) != constants.ID_LENGTH:
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)

    mongo_utility.delete_with_id(constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_AUTHOR, id_value)

    return flask.Response(constants.DELETE_DONE_MESSAGE, status=constants.STATUSCODE_SUCCESS)


@app.route('/vis/top-author', methods=[constants.METHOD_NAME])
def rank_author():
    '''Visualize the ranking of top k highest rated authors.
        :return a response with 200 if the id is valid, a repsonse containing an error message
        and a status code otherwise.'''
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    k_val = flask.request.args.get('k', None)
    try: 
        k_val = int(k_val)

    except ValueError:
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)
        
    top_k_list = mongo_utility.get_top_k_item(constants.COLLECTION_NAME_AUTHOR, k_val)

    return top_k_list, constants.STATUSCODE_SUCCESS

@app.route('/vis/top-book', methods=[constants.METHOD_NAME])
def rank_book():
    '''Visualize the ranking of top k highest rated book.
        :return a response with 200 if the id is valid, a repsonse containing an error message
        and a status code otherwise.'''
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    k_val = flask.request.args.get('k', None)
    try: 
        k_val = int(k_val)

    except ValueError:
        return flask.Response(constants.ID_LENGTH_ERROR, status=constants.STATUSCODE_BAD_REQUEST)
        
    top_k_list = mongo_utility.get_top_k_item(constants.COLLECTION_NAME_BOOK, k_val)

    return top_k_list, constants.STATUSCODE_SUCCESS



if __name__ == '__main__':
    app.run(host='localhost', port=8989)


