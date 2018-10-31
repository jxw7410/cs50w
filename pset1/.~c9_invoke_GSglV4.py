'''
Application.py by Jian Wu
Import order MATTERS
'''
import os
import json
from helpers import *
from errors import *

@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        dbUser = User.query.filter_by(username=username).first()
        if dbUser is None:
            return jsonify({"request": False})

        if not check_password_hash(dbUser.password, password):
            return jsonify({"request": False})

        session["user_id"] = dbUser.id
        return jsonify({"request" : True})

    return render_template("login.html")



@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")


        if password != password_again:
            return jsonify({"request" : False, "errorcode" : 101})

        dbUser = User.query.filter_by(username=username).first()
        if dbUser is None:
            User(username = username, password=generate_password_hash(password)).Add()
            dbUser = User.query.filter_by(username = username).first()

            if dbUser is None:
                return jsonify({"request" : False, "errorcode" : -1})

            session["user_id"] = dbUser.id
            return jsonify({"request" : True})

        return jsonify({"request" : False, "errorcode" : 102})

    return render_template("register.html")



@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html")



@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")



@app.route("/search", methods = ["POST"])
@login_required
def search():
    try:
        book = request.form.get("book")
        if(book.replace(" ", "") is ""):
            raise EmptyInputError
    except EmptyInputError:
        return jsonify({"request" : False})

    if not book:
        return jsonify({"request" : False})

    mem.clear()
    query = paginate_query(CachedQuery().cached(book))
    data = query_items(query.items)
    page_list = paginate_list(query)
    return jsonify({"request" : True, "data" : data, "page_list" : page_list})


@app.route("/getreview")
@login_required
def getreview():
    isbn = request.form.get("isbn")
    return jsonify({"data": fetch_table(isbn)})



@app.route("/selectpage", methods = ["POST"])
@login_required
def selectpage():
    try:
        book = request.form.get("book")
        page = int(request.form.get("page"))
    except ValueError:
        return jsonify({"request" : False})

    query = paginate_query(CachedQuery().cached(book), page)
    data = query_items(query.items)
    page_list = paginate_list(query)
    return jsonify({"request" : True, "data" : data, "page_list" : page_list})


@app.route("/bookinfo", methods = ["GET"])
@app.route("/bookinfo/<isbn>", methods = ["GET"])
@login_required
def bookinfo(isbn=None):
    if isbn:
        get_review = getBookReviewAPI(isbn)
        if get_review:
            create_table(isbn) #only creates a table if it doesn't exist
            query = bookInfoQueryAsync(isbn)

            for item in get_review["book"]:
                query["review_counts"] = item["reviews_count"]
                query["average_score"] = item["average_rating"]

            if review:
                query.update(review)

            return render_template("bookinfo.html", isbnJson = query)

        else:
            return render_template("bookinfo.html")

    else:
        book_isbn = request.args.get("book")
        get_review = getBookReviewAPI(book_isbn)
        if get_review:
            create_table(book_isbn) #only creates a table if it doesn't exist
            query = bookInfoQueryAsync(book_isbn)

            for item in get_review["books"]:
                query["review_counts"] = item["reviews_count"]
                query["average_score"] = item["average_rating"]

            return render_template("bookinfo.html", json = query)

        else:
            return render_template("bookinfo.html")


@app.route("/SubmitReview", methods = ["POST"])
@login_required
def SubmitReview():
    try:
        review = request.form.get("review")
        stars = float(request.form.get("stars"))
        isbn = request.form.get("book")
        if isbn is None:
            raise isbnNullError
    except ValueError:
        return jsonify({"request" : False})
    except isbnNullError:
        return jsonify({"request" : False})

    if insert_table(fetch_table(isbn), review, float("{0:.2f}".format(stars)), session["user_id"]):
        return jsonify({"request" : True})

    return jsonify({"request" : False})



@app.route("/EditReview", methods = ["POST"])
@login_required
def EditReview():
    try:
        review = request.form.get("review")
        stars = float(request.form.get("stars"))
        isbn = request.form.get("book")
        if isbn is None:
            raise isbnNullError
    except ValueError:
        return jsonify({"request" : False})
    except isbnNullError:
        return jsonify({"request" : False})

    if update_table(fetch_table(isbn), review, float("{0:.2f}".format(stars)), session["user_id"]):
        return jsonify({"request" : True})

    return jsonify({"request" : False})


@app.route("/DeleteReview", methods = ["POST"])
@login_required
def DeleteReview():
    try:
        isbn = request.form.get("book")
        if isbn is None:
            raise isbnNullError
    except isbnNullError:
        return jsonify({"request" : False})

    if delete_table(fetch_table(isbn), session["user_id"]):
        return jsonify({"request" : True})

    return jsonify({"request" : False})



@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    if e == 404:
        return render_template("error.html", errorcode = 404), 404
    else:
        return render_template("error.html", errorcode = 500), 500


if __name__ == "__main__":
    app.run()