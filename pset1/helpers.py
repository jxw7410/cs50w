from dbModels import *
from flask import redirect, flash, render_template, request, session, jsonify
from functools import wraps
from tempfile import mkdtemp

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def query_items(pagination):
    list_of_dict = []
    for items in pagination:
        list_of_dict.append(items.dictFormat())
    return list_of_dict



def paginate_list(pagination):
    mdict = {}
    paginate_list = []
    for page in pagination.iter_pages():
        paginate_list.append(page)
    mdict["pages"] = paginate_list
    mdict["current_page"] = pagination.page;
    return mdict



#Doesn't work as intended because the sql code from _query_book was  cached, not the result of the query.
from joblib import Memory
cachedir = mkdtemp()
mem = Memory(cachedir=cachedir)

def paginate_query(query, page = 1, items_per_page = 20):
    return query.paginate(page, items_per_page)

def _query_book(book):
    return Books.query.filter(Books.isbn.like("%" + book + "%"))

class CachedQuery(object):
    def cached(self, book):
        query_book = mem.cache(_query_book)
        return query_book(book)


import requests

def getBookReviewAPI(isbn):
    Key = "98r6Rf0WkYwjZ4Ztr4lNwg"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": Key, "isbns": isbn})
    return res.json()
