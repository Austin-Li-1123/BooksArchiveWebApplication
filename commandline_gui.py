import tkinter
from tkinter import ttk
import main
import util.constants as constants
import util.mongo_utility as mongo_utility

def start_tree_gui():
    '''Construct the tree gui and keep listening for input'''
    app = tkinter.Tk()
    app.title("User interaction")
    ttk.Label(app, text ="Please chooce an action to interact").pack()
    treeview = ttk.Treeview(app)
    treeview.pack()
    tree = treeview

    # construct tree
    treeview.insert('', '0', 'item1', text ='Quries')

    # API methods
    treeview.insert('', '1', 'get', text ='GET')
    treeview.insert('', '2', 'put', text ='PUT')
    treeview.insert('', '3', 'post', text ='POST')
    treeview.insert('', '4', 'delete', text ='DELETE')

    # GET methods
    treeview.insert('get', constants.END_NODE_NAME, constants.GET_BOOK, text ='api/book?id=value', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('get', constants.END_NODE_NAME, constants.GET_AUTHOR, text ='api/author?id=value', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('get', constants.END_NODE_NAME, constants.GET_SEARCH, text ='api/search?q=query', tags=(constants.EVENT_TAG_NAME))

    # PUT methods
    treeview.insert('put', constants.END_NODE_NAME, constants.PUT_BOOK, text ='api/book?id=value', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('put', constants.END_NODE_NAME, constants.PUT_AUTHOR, text ='api/author?id=value', tags=(constants.EVENT_TAG_NAME))

    # POST methods
    treeview.insert('post', constants.END_NODE_NAME, constants.POST_BOOK, text ='api/book', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('post', constants.END_NODE_NAME, constants.POST_BOOKS, text ='api/books', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('post', constants.END_NODE_NAME, constants.POST_AUTHOR, text ='aapi/author', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('post', constants.END_NODE_NAME, constants.POST_AUTHORS, text ='api/authors', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('post', constants.END_NODE_NAME, constants.POST_SEARCH, text ='api/scrape?attr=value', tags=(constants.EVENT_TAG_NAME))

    # delete methods
    treeview.insert('delete', constants.END_NODE_NAME, constants.DELETE_BOOK, text ='api/book?id=value', tags=(constants.EVENT_TAG_NAME))
    treeview.insert('delete', constants.END_NODE_NAME, constants.DELETE_AUTHOR, text ='api/author?id=value', tags=(constants.EVENT_TAG_NAME))

    # Placing each child items in parent widget
    treeview.move('get', 'item1', constants.END_NODE_NAME)
    treeview.move('put', 'item1', constants.END_NODE_NAME)
    treeview.move('post', 'item1', constants.END_NODE_NAME)
    treeview.move('delete', 'item1', constants.END_NODE_NAME)

    # bind events
    def call_back(event):
        parse_commandline_input(tree.selection()[0])

    treeview.tag_bind(constants.EVENT_TAG_NAME, '<<TreeviewSelect>>', call_back)
    app.mainloop()

def parse_commandline_input(selection):
    '''parse the treemenu selection and call the corresponding function in main.py
        :param selection: the field of the tree that is being selected'''
    # get_book or get_author
    if selection == constants.GET_BOOK or selection == constants.GET_AUTHOR:
        obj_id = input("Please input the id of qury")
        json_data = mongo_utility.search_with_id(constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_BOOK, obj_id)
        print(json_data)

    elif selection == constants.PUT_BOOK or selection == constants.PUT_AUTHOR:
        # put, call the json_update function
        json_filename = input("Please input the path of JSON file")
        main.parse_parameter(["json_update", json_filename])

    elif selection == constants.POST_BOOK or selection == constants.POST_AUTHOR or selection == constants.POST_BOOKS or selection == constants.POST_AUTHORS:
        # post, call the json_create function
        json_filename = input("Please input the path of JSON file")
        main.parse_parameter(["json_create", json_filename])

    elif selection == constants.DELETE_BOOK or selection == constants.DELETE_AUTHOR:
        # delete, call delete function in mongo_utility
        obj_id = input("Please input the id of qury")
        json_data = mongo_utility.delete_with_id(constants.DATABASE_NAME_MAIN, constants.COLLECTION_NAME_BOOK, obj_id)

if  __name__ =='__main__':
    start_tree_gui()