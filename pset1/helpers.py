from dbModels import *
from functools import wraps

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



def paginate_query(query, page = 1, items_per_page = 20):
    return query.paginate(page, items_per_page)

def query_book(book):
    return Books.query.filter(Books.isbn.like("%" + book + "%"))

def getusername(sessionid):
    return User.query.filter_by(id = sessionid).first().GetUserName()


import requests

def getBookReviewAPI(isbn):
    Key = "98r6Rf0WkYwjZ4Ztr4lNwg"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": Key, "isbns": isbn})
    return res.json()


def bookInfoQueryAsync(isbn):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = loop.run_until_complete(asyncio.gather(bookqueryAsync(isbn),
                                    reviewqueryAsync(isbn, getusername(session["user_id"]))))
    loop.close()

    if tasks[1]:
        query = tasks[0]
        query.update(tasks[1])
    else:
        query = tasks[0]
    return query


async def bookqueryAsync(isbn):
    res = Books.query.filter_by(isbn = isbn).first().dictFormat()
    await asyncio.sleep(0)
    return res


async def reviewqueryAsync(isbn, user):
    res = get_table_data(fetch_table(isbn), user)
    await asyncio.sleep(0)
    return res

