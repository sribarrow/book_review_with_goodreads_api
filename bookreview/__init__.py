import os

from flask import Flask, session
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
app.config['SECRET_KEY']='53e83c3ea1dcec9f20607eedbef91fbb'
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#csrf = CSRFProtect(app)
bcrypt=Bcrypt(app)
logman=LoginManager(app)
logman.login_view = 'login'
logman.login_message_category = 'info'

db = SQLAlchemy()
db.init_app(app)
engine = create_engine(os.getenv("DATABASE_URL"))
con = scoped_session(sessionmaker(bind=engine))

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

from bookreview import routes