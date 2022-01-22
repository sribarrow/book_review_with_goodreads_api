import csv
from my_app import db
from my_app.models import Book

with open('data/books.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        book=Book(title=row['title'], isbn=row['isbn'], author=row['author'], year=row['year'])
        db.session.add(book)

db.session.commit()