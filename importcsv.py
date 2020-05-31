import csv
from bkreview import db
from bkreview.models import Book

with open('data/books.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        book=Book(title=row['title'], isbn=row['isbn'], author=row['author'], year=row['year'])
        db.session.add(book)

db.session.commit()