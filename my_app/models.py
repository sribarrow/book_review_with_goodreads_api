from datetime import datetime
from time import time
import jwt
from my_app import Flask, app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__='person'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_login=db.Column(db.DateTime, nullable=True)  
    remember=db.Column(db.Boolean, nullable=True)
    usr_reviews = db.relationship("Review", backref="reviewer", lazy=True)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Person.query.get(id)

    def __repr__(self):
        """Define a base way to print models"""
        return f"Person('{self.username}, {self.email})"


class Book(db.Model):
    __tablename__='book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    bk_reviews = db.relationship("Review", backref="bkreview", lazy=True)

    def __repr__(self):
        """Define a base way to print models"""
        return f"Book('{self.title}, {self.isbn}, {self.year}, {self.author})"
  
class Review(db.Model):
    __tablename__='review'
    id = db.Column(db.Integer, primary_key=True)
    rating=db.Column(db.Integer, nullable=False)
    comments=db.Column(db.Text, nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False)
    userid=db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    bookid=db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    def __repr__(self):
        """Define a base way to print models"""
        return f"Review('{self.book}, {self.isbn}, {self.comments}, {self.userid}, {self.date_posted})"
