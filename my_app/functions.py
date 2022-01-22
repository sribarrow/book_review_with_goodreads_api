from flask_mail import Message
from my_app import mail
from flask import render_template

import re, json, requests

from my_app.models import Person

# functions
# read using goodreads API
def get_from_goodreads(isbn):
    json_data = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "F7hsZWBdSYPjK2YAVnQQ", "isbns": {isbn}})
    res =  json_data.json()
    return res

# send mail
def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    #msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = Person.get_reset_password_token(user)
    send_email('[Book Review app] Reset Your Password',
               sender='no-reply@test.com',
               recipients=[user.email],
               html_body=render_template('reset_password.html',
                                         user=user, token=token))


# validations functions using regular expression

def validate_email(email):
    expr='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)'
    p=re.compile(expr)
    return p.search(email)

def validate_username(uname):
    expr='(^[a-zA-Z0-9]{4,20}$)'
    p=re.compile(expr)
    return p.search(uname)

def validate_password(pwd):
    expr='^(?=.{8,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$'
    p=re.compile(expr)
    return p.search(pwd)

def match_password(p, cp):
    if p == cp:
        return True
    else:
        return False