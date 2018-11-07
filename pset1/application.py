'''
Application.py by Jian Wu
Import order MATTERS
'''
import os
import json
from helpers import *

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
        session["username"] = username
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
    return render_template("index.html", user = session["username"])



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


@app.route("/api", methods = ["GET"])
@login_required
def getapi():
    try:
        isbn = request.args.get("isbn")
    except:
        return render_template("getapi.html")

    get_review = getBookReviewAPI(isbn)
    if get_review:
        query = Books.query.filter_by(isbn = isbn).first().dictFormat()
        for item in get_review["books"]:
            query["review_counts"] = item["reviews_count"]
            query["average_score"] = item["average_rating"]
        return render_template("getapi.html", json = query)
    return render_template("getapi.html")



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


@app.route("/bookinfo")
@login_required
def bookinfo():
    try:
        book_isbn = request.args.get("book")
    except:
        return render_template("bookinfo.html")

    get_review = getBookReviewAPI(book_isbn)
    if get_review:
        create_table(book_isbn) #only creates a table if it doesn't exist
        query = bookInfoQueryAsync(book_isbn)

        for item in get_review["books"]:
            query["review_counts"] = item["reviews_count"]
            query["average_score"] = item["average_rating"]

        session["other_posts_counter"] = 6 if session["user_id"] > 5 else 7
        return render_template("bookinfo.html", json = query, user = session["username"])

    else:
        return render_template("bookinfo.html", user = session["username"])


@app.route("/SubmitReview", methods = ["POST"])
@login_required
def SubmitReview():
    try:
        review = request.form.get("review")
        stars = float(request.form.get("stars"))
        isbn = request.form.get("book")
        date = request.form.get("date")
        if isbn is None:
            raise isbnNullError
        if date is None:
            raise dateNullError
    except ValueError:
        return jsonify()
    except isbnNullError:
        return jsonify()
    except dateNullError:
        return jsonify()

    if insert_table(fetch_table(isbn), review, float("{0:.2f}".format(stars)), date, session["username"]):
        return jsonify({"request" : True})

    return jsonify()



@app.route("/EditReview", methods = ["POST"])
@login_required
def EditReview():
    try:
        review = request.form.get("review")
        stars = float(request.form.get("stars"))
        isbn = request.form.get("book")
        date = request.form.get("date")
        if isbn is None:
            raise isbnNullError
        if date is None:
            raise dateNullError
    except ValueError:
        return jsonify()
    except isbnNullError:
        return jsonify()

    if update_table(fetch_table(isbn), review, float("{0:.2f}".format(stars)), date, session["username"]):
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

    if delete_table(fetch_table(isbn), session["username"]):
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

    data = get_table_data_other_users(fetch_table(isbn), session["username"])
    if data:
        return jsonify({"data" : data})

    return jsonify()

@app.route("/nextreview", methods = ["POST"])
@login_required
def nextreview():
    try:
        isbn = request.form.get("book")
        if isbn is None:
            raise isbnNullError
    except isbnNullError:
        return jsonify()
    id_ref = session["other_posts_counter"] if session["other_posts_counter"] is not session["user_id"] else session["other_posts_counter"] + 1
    data = get_next_review(fetch_table(isbn), id_ref)
    if data:
        session["other_posts_counter"] = id_ref + 1
        return jsonify({"data" : data})

    session["other_posts_counter"] = id_ref
    return jsonify()

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
    app.run(debug=True, use_reloader=False)