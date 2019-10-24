import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, lm
from flask_login import UserMixin
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, and_, or_, func

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User {0}>'.format(self.username)

@lm.user_loader
def load_user(id):
    if id=='None' or id is None:
        id=-1 # it is id for guests and anonymous user
    return User.query.get(int(id)) 



class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(100))
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.String(4))

    
    def add_book(isbn, title, author, year):
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()
    
    @staticmethod
    def search(search, page):
        books =  Book.query.filter(\
                 or_(Book.title.like(f'%{search}%'),\
                     Book.isbn.like(f'%{search}%'),\
                     Book.author.like(f'%{search}%'),\
                     Book.year.like(f'%{search}%') \
                 )).paginate(page, per_page=10)
        return books

    
class Review(db.Model):
    __tablename__ = 'reviews'
    book_id = db.Column(db.Integer, ForeignKey('books.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        PrimaryKeyConstraint(
            book_id,
            user_id),
        {})
    
    
    @staticmethod
    def is_exists(book_id, user_id):
        exists = Review.query.filter(
            and_(Review.user_id == user_id,
                 Review.book_id == book_id)).first()
        if exists:
            return True
        else:
            return False

    @staticmethod
    def register(book_id, user_id, rating, comment):
        review = Review(book_id=book_id, user_id=user_id, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()


