# Project 1

CS50 - Web Programming with Python and JavaScript

Database in Heroku
models.py - contains db object definitions
Create DB Objects:
- From python commandline
    -- from my_app import db
    -- db.drop_all()
    -- db.create_all()

Project Tree
-------------
Root - BOOK_REVIEW
books.csv - Project file
importcsv.py - imports books.csv into book table
requirements.txt - contains list of packages installed used in the project
runapp.py - application file.

my_app - application package
__init__.py - default for python packages. app and other applicaiton variables initialised here
static - dir - contains image dir and css
templates - web/html files
- layout.html - blueprint for the project html files extended to all html files
- about.html - Project description
- book.html - book info display page
- change_password.html - allows user to change password
- forgot_password - linked from login page, initiates email link for password reset
- help.html - help & usage for API and goodreads extract
- index.html - homepage - lists top 10 books with reviews - book title linked to book page for more details on the book
- login.html - Allows user to login
- register.html - Allows user to register
- reset_password.html - Template sent to user as email to change password
- search.html - Allows user to search for books by 

CSS - bootstrap and static/main.css


General Setup:
    - package app
    - init__.py to initialise application variables
    - models.py

Static pages
    - About page - about.html
    - API page - help documentation 

Run app - python runapp.py

1) Registration
    file - register.html
    Fields - username, email, password
    Additional:
          i) password is hashed
         ii) field validation (using regex)
    Note:
    - Forgot password - emulate mail server 
    $ python -m smtpd -n -c DebuggingServer localhost:8025
    
2) Login
    file - login.html
    Fields - email, password, remember me
    Additional:
          i) sets session variables to track current user
         ii) set cookies to remember last login 
        iii) takes user to home page with last 10 reviews

3) Logout 
    unsets session variables

4) Import
    file - importcsv.py

5) search 
    file - search.html
    - login required
    - wildcard search
    - links to book details page

6) book page
    file - book.html
    - displays Book info and related reviews

7) Review submission
    file - book.html
    Logged in users can add reviews. Reviews are unique for a book and user (single review allowed per user per book).

8) API
   - get request
   - takes an isbn
   - provides book info as json 
   - help.html

9) Goodread
    - pulls data for a given book in json format
    - extracts the ratings info as additional info to book page
    - 

10) Youtube - https://youtu.be/dDDtRJSa9c0


PROJECT TREE
=============
.
├── README.md
├── __pycache__
│   └── runapp.cpython-38.pyc
├── books.csv
├── flask_session
│   ├── 2029240f6d1128be89ddc32729463129
│   └── e837464f0492db95c71018220b2b22ae
├── importcsv.py
├── my_app
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   ├── functions.cpython-38.pyc
│   │   ├── models.cpython-38.pyc
│   │   └── routes.cpython-38.pyc
│   ├── functions.py
│   ├── models.py
│   ├── pkgs-installed.txt
│   ├── routes.py
│   ├── static
│   │   ├── images
│   │   │   └── book.jpg
│   │   └── main.css
│   └── templates
│       ├── about.html
│       ├── book.html
│       ├── change_password.html
│       ├── forgot_password.html
│       ├── help.html
│       ├── index.html
│       ├── layout.html
│       ├── login.html
│       ├── register.html
│       ├── reset_password.html
│       └── search.html
├── requirements.txt
└── runapp.py

Installed apps
==============
alembic==1.4.2
bcrypt==3.1.7
blinker==1.4
cachelib==0.1
certifi==2020.4.5.1
cffi==1.14.0
chardet==3.0.4
click==7.1.2
dnspython==1.16.0
email-validator==1.0.5
Flask==1.1.2
Flask-Bcrypt==0.7.1
Flask-Login==0.5.0
Flask-Mail==0.9.1
Flask-Migrate==2.5.3 - not used
Flask-Script==2.0.6
Flask-Session==0.3.2
Flask-SQLAlchemy==2.4.1
Flask-Validator==1.4.1 - not used
Flask-WTF==0.14.3 
idna==2.9
isbnlib==3.9.10
iso3166==1.0.1
itsdangerous==1.1.0 - not used
Jinja2==2.11.2
Mako==1.1.2
MarkupSafe==1.1.1
psycopg2-binary==2.8.5
py-moneyed==0.8.0
pycparser==2.20
PyJWT==1.7.1
python-dateutil==2.8.1
python-editor==1.0.4
pytz==2019.3
requests==2.23.0
schwifty==2020.2.2
simplejson==3.17.0
six==1.14.0
SQLAlchemy==1.3.17
urllib3==1.25.9
Werkzeug==1.0.1
WTForms==2.3.1