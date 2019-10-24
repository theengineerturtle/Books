import json
from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User, Book, Review
from . import main
from .forms import LoginForm, SearchForm, ReviewForm
import requests
from flask import jsonify


@main.route('/')
def index():
    clear_search_session() 
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    clear_search_session()    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Check your username/password')
            return redirect(url_for('main.login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    clear_search_session() 
    form = LoginForm()
    
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('This username is in use.')
            return redirect('signup', **request.args)
        if len(form.password.data) < 3:
            flash('The password should at least 4 characters')
            return redirect('signup', **request.args)
        
        try:
            User.register(form.username.data, form.password.data)
            flash('Account created successfully.')
        except:
            flash('Account could not created, failed')

    return render_template('signup.html', form=form)


@main.route('/logout')
@login_required
def logout():
    clear_search_session() 
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    form = SearchForm()
    page = request.args.get('page', 1, type=int)
        
    if form.validate_on_submit():
        search = form.searchtext.data
        session['search'] = search
    # this is works but not a best practice, store search variable in session
    if not 'search' in session:
        search = ''
    else:
        search = session.get('search') 
    
    books = Book.search(search, page)
    
    return render_template('search.html', books=books, form=form)    


def clear_search_session():
    if 'search' in session : 
        session['search'] = ''


@main.route('/apidocs')
def apidocs():
    return render_template('apidoc.html')


@main.route('/books/<int:bookid>', methods=['GET', 'POST'])
@login_required
def bookdetail(bookid):
    
    book = Book.query.filter_by(id=bookid).first()       
    
    goodreads_reviews = {} 

    form = ReviewForm()
    exist = None
    comment = None
    rating = None

    if form.validate_on_submit():
        comment = form.comment.data
        rating = int(form.rating.data)
        
        exist = Review.is_exists(book_id=book.id, user_id=current_user.id)
        
        if not exist:
            try:
                Review.register(book.id, current_user.id, rating, comment)
            except:
                flash('Review register function error')
                return redirect(request.url)
        else:
            flash('You have already comment out for this book.')
            return redirect(request.url)
    if book:
        try:
            requestpost = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ILtGvk39LV61VNVPKoBYew", "isbns": book.isbn })
            response_data = requestpost.json()
            goodreads_reviews = {'work_ratings_count':response_data["books"][0]["work_ratings_count"],
                                 'average_rating': response_data["books"][0]["average_rating"]}    
        except Exception as e:
            pass

    #show the reviews for this book by all users
    if book:
        bookid = book.id
        users_reviews = Review.query.filter_by(book_id=bookid)

        user_review_data = list()
        
        for user_review in users_reviews:
            user = User.query.get(user_review.user_id)
            r={}
            r['comment'] = user_review.comment
            r['username'] = user.username
            r['rating'] = user_review.rating
            user_review_data.append(r)      

        # dict to json
        user_review_data = json.dumps(user_review_data)
        user_review_data = json.loads(user_review_data)

    return render_template('bookdetail.html', form=form, book=book, goodreads_reviews = goodreads_reviews, user_review_data=user_review_data)


@main.route('/api/<string:isbn>')
def api_get_info_by_isbn(isbn):

    book = Book.query.filter_by(isbn=isbn).first()
    reviews = {}
    if book:
        reviews = Review.query.filter_by(book_id=book.id).all()
    if book == None or reviews == None:
        return render_template('error.html', message="404 Not Found")
    else:
        review_count = 0
        average_score = 0
        sum_rating = 0
        for review in reviews:
            sum_rating += review.rating
        review_count = len(reviews)
        if sum_rating>0:
            average_score = sum_rating/review_count


        return jsonify({
            "title": book.title,
            "author": book.author,
            "year" : book.year,
            "review_count" : review_count,
            "average_score" : average_score
            })
    return render_template('apidoc.html')
