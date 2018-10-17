'''
Application.py by Jian Wu
Import order MATTERS
'''
import os
from helpers import *


'''
Original source code had SQLAlchemy engine, but if flask quick start (in dbModels) is available, don't need engine
check out the page SQLAchemy flask, it basically does some configurations for users with regards to SQLAlchemy.session
'''

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
    book = request.form.get("book")

    if not book:
        return jsonify({"request" : False})

    mem.clear()
    query = paginate_query(CachedQuery().cached(book))
    data = query_items(query.items)
    page_list = paginate_list(query)
    return jsonify({"request" : True, "data" : data, "page_list" : page_list})



@app.route("/bookinfo", methods = ["GET", "POST"])
@login_required
def bookinfo(isbn):
    return render_template("bookinfo.html", isbn = isbn)


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



if __name__ == "__main__":
    session.clear()
    app.run()