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
            return jsonify()

        if not check_password_hash(dbUser.password, password):
            return jsonify()

        session["user_id"] = dbUser.id
        return jsonify({"request" : True})

    return render_template("login.html")



@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("passwordAgain")

        if password != password_again:
            return jsonify({"errorcode" : 101})

        dbUser = User.query.filter_by(username=username).first()
        if dbUser is None:
            User(username = username, password=generate_password_hash(password)).Add()
            dbUser = User.query.filter_by(username = username).first()

            if dbUser is None:
                return jsonify({"errorcode" : -1})

            session["user_id"] = dbUser.id
            return jsonify({"request" : True})

        return jsonify({"errorcode" : 102})

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
        return jsonify()

    if not book:
        return jsonify()

    query = paginate_query(query_book(book))
    data = query_items(query.items)
    page_list = paginate_list(query)
    return jsonify({"data" : data, "page_list" : page_list})


@app.route("/getrawreview")
@login_required
def getrawreview():
    isbn = request.form.get("isbn")
    return jsonify({"data": fetch_table(isbn)})



@app.route("/selectpage", methods = ["POST"])
@login_required
def selectpage():
    try:
        book = request.form.get("book")
        page = int(request.form.get("page"))
    except ValueError:
        return jsonify()

    query = paginate_query(query_book(book), page)
    data = query_items(query.items)
    page_list = paginate_list(query)
    return jsonify({"data" : data, "page_list" : page_list})


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
        return jsonify()
    except isbnNullError:
        return jsonify()

    if insert_table(fetch_table(isbn), review, float("{0:.2f}".format(stars)), getusername(session["user_id"])):
        return jsonify({"request" : True})

    return jsonify()



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
        return jsonify()
    except isbnNullError:
        return jsonify()

    if update_table(fetch_table(isbn), review, float("{0:.2f}".format(stars)), getusername(session["user_id"])):
        return jsonify({"request" : True})

    return jsonify()


@app.route("/DeleteReview", methods = ["POST"])
@login_required
def DeleteReview():
    try:
        isbn = request.form.get("book")
        if isbn is None:
            raise isbnNullError
    except isbnNullError:
        return jsonify()

    if delete_table(fetch_table(isbn), getusername(session["user_id"])):
        return jsonify({"request" : True})

    return jsonify()


@app.route("/GetFewReviews", methods = ["POST"])
@login_required
def GetFewReviews():
    try:
        isbn = request.form.get("book")
        if isbn is None:
            raise isbnNullError
    except isbnNullError:
        return jsonify()

    return jsonify({"data" : get_table_data_other_users(fetch_table(isbn), getusername(session["user_id"]))})


@app.route("/Error", methods = ["POST"])
@login_required
def Error():
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