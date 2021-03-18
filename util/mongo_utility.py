import pymongo
from bson.json_util import dumps
import bson
import operator
import json
import util.constants as constants

def insert_json_to_mongo(json_string, database_name, collection_name):
    '''post a json string to the mongoDB database
        :param json_string: in the form: {'a': 'b', ...}
        :param database_name: 1. test, 2. sp21-cs242-assignment2.0
        :param collection_name: 1. Books, 2. Authors
        :return The id of the inserted object on the server'''
    database = constants.MONGO_CLIENT[database_name]

    collection = database[collection_name]
    post_id = collection.insert_one(json_string).inserted_id

    return post_id

def search_and_update(json_obj, database_name, collection_name):
    '''search an object by the id field and update its information
        :param json_obj: in the form: {'a': 'b', ...}
        :param database_name: 1. test, 2. sp21-cs242-assignment2.0
        :param collection_name: 1. Books, 2. Authors'''
    database = constants.MONGO_CLIENT[database_name]
    collection = database[collection_name]
    id_string = list(json_obj["_id"].values())[0]
    del json_obj["_id"]

    data_found = search_with_id(database_name, collection_name, id_string)
    collection.update_one(data_found, {"$set": json_obj})

    print(f"PROGRESS: Updated _id: {id_string} from JSON")

def search_with_id(database_name, collection_name, id_string):
    '''search an object by the id field and return it
        :param id_string: id of the object requested
        :param database_name: 1. test, 2. sp21-cs242-assignment2.0
        :param collection_name: 1. Books, 2. Authors
        :return the json obj with that id. None if id not found'''
    database = constants.MONGO_CLIENT[database_name]
    collection = database[collection_name]

    return collection.find_one(bson.ObjectId(id_string))

def delete_with_id(database_name, collection_name, id_string):
    '''search an object by the id field and delete it
        :param id_string: id of the object requested
        :param database_name: 1. test, 2. sp21-cs242-assignment2.0
        :param collection_name: 1. Books, 2. Authors
        :return Number of items deleted. None if id not found'''
    database = constants.MONGO_CLIENT[database_name]
    collection = database[collection_name]

    return collection.delete_one({"_id": bson.ObjectId(id_string)})

def download_to_json(file_name):
    '''Download the specified number of books and authors to the desinated JSON file
        :param file_name: Name of the file to to download data into'''
    database = constants.MONGO_CLIENT[constants.DATABASE_NAME_MAIN]

    collection_book = database[constants.COLLECTION_NAME_BOOK]
    download_helper(file_name, collection_book, True)

    collection_author = database[constants.COLLECTION_NAME_AUTHOR]
    download_helper(file_name, collection_author, False)

def download_helper(file_name, collection, is_first):
    '''helper function of download_to_json. gets the data from a collection on mongodb and stores to a JSON file
        :param file_name: Name of the file to to download data into
        :param collection: The reference of the collection on server
        :param is_first: If true, open with mode write, else mode append'''
    cursor = collection.find()
    list_cur = list(cursor)
    json_data = dumps(list_cur, indent = 2)

    if is_first:
        with open(file_name, 'w') as file:
            file.write(json_data)
    else:
        with open(file_name, 'a') as file:
            file.write(json_data)

def get_top_k_item(collection_name, k):
    '''Get k highest ranked author
        :param k: The number of top items requested
        :param collection_name: The reference of the collection on server'''
    author_dict = {}
    database = constants.MONGO_CLIENT[constants.DATABASE_NAME_MAIN]
    collection = database[collection_name]
    cursor = collection.find({})
    for document in cursor:
        author_dict[document["name"]] = document["rating"]

    # return the top k items
    sorted_dict = sorted(author_dict.items(), key=operator.itemgetter(1))
    top_k_dict = reverse_list(sorted_dict[-k:])

    return dict(top_k_dict)

def reverse_list(input_list): 
    '''Reversing a list using reversed() 
        :param input_list: The input list to be reversed'''
    return [item for item in reversed(input_list)] 