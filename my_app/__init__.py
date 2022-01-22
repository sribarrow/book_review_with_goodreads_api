import os

from flask import Flask, session
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SECRET_KEY']='53e83c3ea1dcec9f20607eedbef91fbb'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
app.config['JSON_SORT_KEYS'] = False

global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*60*1 #1 hr

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAIL_SERVER"]="localhost"
app.config["MAIL_PORT"]="8025"

session=Session(app)
csrf = CSRFProtect(app)
bcrypt=Bcrypt(app)
mail = Mail(app)

db = SQLAlchemy()
db.init_app(app)

# # Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

from my_app import routes