## Books API - Search and Review

### Installation

To run the program, assure Python 3 and Pip are installed ([check this link if Python 3 is not installed](https://www.python.org/downloads/) and [this link if Pip is not installed](https://pip.pypa.io/en/stable/installation/)).

After both are installed, go to the project directory within your terminal and run the following command:

`pip3 install -r requirements.txt`

After the package installation is finished, the project is set up and ready to run.


### Running the server

In the project directory, run the following commands:
```
cd src

uvicorn main:app
```
The application is now accessible at the following address `http://127.0.0.1:8000`

To access the Interactive API Docs, visit `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`

### The API

You can send requests to Gutendex to query books by their' title or ID. These requests are cached for 60 seconds.

You can also submit reviews and ratings for a given book. These will be stored locally using SQLite as the Database.

The API can also provide a list of top-rated books and the monthly average rating for a given book.

### Tests

To run the tests run the following command in the root of the project:

`pytest`
