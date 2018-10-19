'''
Application.py by Jian Wu
Import order MATTERS
'''
import os
from helpers import *


@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        dbUser = User.query.filter_by(username=username).first()
        '''
        newtable = fetch_table(userdbEngine, "test1")
        connection = userdbEngine.connect()
        connection.execute(newtable.insert(values=dict(Value='this')))
        connection.close()
        '''
        print(sessionengine.query(newtable).all())
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
    book = request.form.get("book")
    if not book:
        return jsonify({"request" : False})

    mem.clear()
    query = paginate_query(CachedQuery().cached(book))
    data = query_items(query.items)
    page_list = paginate_list(query)
    return jsonify({"request" : True, "data" : data, "page_list" : page_list})



@app.route("/bookinfo")
@app.route("/bookinfo/<isbn>")
@login_required
def bookinfo(isbn=None):
    if isbn:
        return render_template("bookinfo.html")

    book_isbn = request.args.get("book")
    getBookReviewAPI(book_isbn)

    return render_template("bookinfo.html")


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
    session.clear()
    app.run()