from datetime import datetime

# from flask import Flask
from bookreview import db, logman
from flask_login import UserMixin

@logman.user_loader 
def load_user(user_id):
    return Person.query.get(int(user_id))

class Person(db.Model, UserMixin):
    __tablename__='person'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_login=db.Column(db.DateTime, nullable=True)  
    usr_reviews = db.relationship("Review", backref="reviewer", lazy=True)

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
