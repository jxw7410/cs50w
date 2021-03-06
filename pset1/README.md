# Project 1

Web Programming with Python Flask Framework and JavaScript

Note:
Technically Project 1 does not require the use of JavaScript, but relying on pure static page rendering via Flask.
However, my version incorporates JavaScript, while satisfying the scope of the project. Also I did not use PostSQL, but SQLite
since it was more convenient. However in exchange for that convenience, something inconvenient happens later. FYI, the only prior
experience I have to web programming is the initial cs50 course. If you see something that is abnormal for a beginner, it's probably
because it was something I adapted from stackoverflow, and other sources, not without understanding of course.

Brief Summary:
Database Folder -
The database folder contains 3 database files, which has a database for users registry, book library, and book review information.
It was intentionally done this way to create order. Furthermore, there is importance in seperating the book review informations from the
other two database. The importance is that there isn't actually a static class object that is mapped to a book review for a particular
book, instead when the user clicks on a book, a table is dynamically generated, and mapped to that book, (and if the book isn't registered
in the database, it's done so). A function returns a metadata table reference to the book, and that table reference will be used to
reference the book in the bookreviews.db to access the user review, as well as reviews of other users.

Static -
The static folder contains two files, a css file, and a js file. The css file is self-explanatory, and it only serves to style the html
elements in various pages.

The JS file contains mostly AJAX request to backend server to dynamically load data, which would otherwise take along time, if the data
rendering was done statically. Some of these data loading are very heavy operations. For example, when the user is using the search bar
in the index.html page, what happens is a pagination of the data the user wants is loaded from the backend, dynamically. This is important
because there is alot of styling involved for the data when the HTML code is loaded, so if a user wants a generate search for everything,
imagine 5000 data points, and each of them have to be styled in a table; this would take too long to be practical. Pagination returns
only a number of data at a time as the user goes through the pages. A pseudo-cache is also impended the front end, which stores the data
set requested from the server, so when the user access a previous page, the data from the cache is loaded instead.

In the bookinfo.html, AJAX is also used to dynamically load user reviews, and as the user continues to scroll down, a new review, until the
last review, is continuously loaded.

Template-
Contains all HTML pages

Python Files-
There are alot of python files, but they can all technically be incoporated as one. However, in doing so, it would harder to maintain
the code, so the files were seperated, however with a particular import order so mimic a singular python file. The import order
goes init_config && errors -> dbModels -> helpers -> application. The other file import.py only serves as a import script to import a csv
file into a database file.
init_config.py initializes the flask framework, and sqlalchemy for ORM.
error.py contains a series of custom error flags to handle errors, to prevent the pages from crashing. Not all errors are accounted for.
dbModels.py contains the models for ORM, as well as the helper functions specific to ORM
helper.py contains functions that help process data better, for example, there are async functions written to access seperate databases
to get information, and merge the information together.
application.py contains the routes, and otherwise, the main code of the web app.

Other notes:
Earlier I mentioned that I used sqlite instead of PostSQL for convenience, only to encounter something inconvenient. So, in the bookinfo.html,
I mentioned that user reviews are dynamically generated from the database as the user continues to scroll down. Each review contains a ID
that is based off the user-ID, so what really is happening is that a reference to "User-ID" of all users runs in the backend, and as the user scrolls
down, the reference increments (and if the reference is the same as the current session user, it is skipped). Because of how the table design,
the reviews are always ordered by ID by default, which is okay for the scope of this project. However, what if in the future, I decided to implement
a sort by date, or whatever factor, function? There are options, such as sending the data to the front end, and let the JS handle the sorting,
or secondly, parse the database in sorted manner, and load each new reviews by row number instead of a particular column. The problem is SQLite
is not capable of doing Row_Number() Order_By properly, as the SQL code generated by SQLAlchemy raises an error in SQLite.

