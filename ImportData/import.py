import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///' + os.path.join(
        os.path.dirname(__file__), '../data.sqlite3'))

db = scoped_session(sessionmaker(bind=engine))

def importBook():
    f = open("books.csv")
    reader = csv.reader(f)
    i=1
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn":isbn, "title":title, "author":author, "year":year})
        print(f"{i}. book added:{isbn}, title:{title}, author:{author}, year:{year}")
        i = i + 1
    db.commit()

if __name__ == "__main__":
    importBook()

