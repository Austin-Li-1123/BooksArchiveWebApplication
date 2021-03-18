# sp21-cs242-assignment2

## Files and contents
**main.py**: Main method parses the parameters, decides which mode to run in and execute by utilizing function from other modules.  
**commandline_gui.py**: The GUI that supports GET, PUT, POST, and DELETE.   
**utility.py**: Utility functions for the other files to use.  
**mongo_utility.py**: Utility functions using mongoDB API.  
**constants.py**: Contains all constants and macros used by the program.  
**unit_tests.py**: Unit tests for the command line interface and utility functions.  
**interpreter_tests.py**: Unit tests for the interpreter and qury classes.  
**web_frontend**: Folder contains the frontend implementation which works with the backend flask server.

## How to run
**Run command line GUI** python3 commandline_gui.py  
**To scrape**: python3 main.py scrape (Start URL) (#books) (#authors)  
**To download** python3 main.py download (json filename)  
**To update database** python3 main.py json_update (json filename)  
**To add to database** python3 main.py json_create (json filename)  
