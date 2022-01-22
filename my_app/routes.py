from my_app import app, db, bcrypt, csrf, COOKIE_TIME_OUT
from flask import request, render_template, url_for, flash, redirect, session, jsonify
from my_app.models import Person, Book, Review, datetime
from my_app.functions import *

#create empty message list to post validation errors
#messages={}
## homepage
## shows top 10 reviews. (Cannot add reviews without sign in)
@app.route("/")
def index():
    if 'current_user' in session:
        username=session['current_user']
        books=db.execute(f"select t.id, t.title, t.author, round(avg(t.rating),1) rating, count(1) reviews "
                        "from  (select b.id, b.title, b.author, r.rating from review r, book b "
                        "where r.bookid=b.id "
                        "order by date_posted desc) t "
                        "group by 1,2,3  order by rating desc, reviews desc  limit 10")
        return render_template('index.html', books=books, title="Book Reviews")
    else:
        return redirect(url_for('login'))

# project summary page
@app.route("/about")
def about():
    return render_template('about.html', title="About Us")

# API help
@app.route("/api/help")
def help():
    return render_template('help.html', title="API documentation")
    
# search page - login required.
# user can search books by title, isbn or author - allows wildcard search
# retrieves top 10 results (can be improved with pagination)
@app.route("/search",  methods=['GET','POST'])
def search():
    if 'current_user' in session:
        if request.method == 'POST':
            option=request.form.get('select')
            text=  request.form.get('search-text')
            if request.form.get("search-text") == '':
                flash(f"Search string cannot be empty.", "danger")
                return(redirect(url_for('search')))
            else:
                results=db.execute(f"select * from book where {option} ilike '%{text}%' limit 10").fetchall()
                #print(f"select * from book where lower({option}) like '%{text.lower()}%'")
                return render_template('search.html', title="Book list", results=results)
        else:
            return render_template('search.html', title="Book list")
    else:
        flash(f"Login to search for books to review", 'info')
        return redirect(url_for('login'))

## book page
## displays book details with user reviews
## From homepage, user can view individual book details (login not required)
## from search page user can view reviews (login not required)
## Only signed in user can add reviews
@app.route("/books/<int:book_id>",methods=['GET','POST'])
def book(book_id):
    if request.method == 'POST':
        if 'current_user' in session:
            if request.form.get("review-text") == '':
                flash(f"Review cannot be empty.", "danger")
                return(redirect(url_for('book', book_id=book_id)))
            else:
                text = request.form.get('review-text')
                rating= request.form.get('rating')
                user=session['user_id']
                result=db.execute(f"select * from review where userid={user} and bookid={book_id}").fetchall()
                
                if result :
                    flash("Review not added. You have already reviewed this book.", "info")
                    return(redirect(url_for('book', book_id=book_id)))   
                else:
                    db.execute(f"insert into review (userid, bookid, comments, rating, date_posted) values ({user}, {book_id}, '{text}', {rating}, '{datetime.utcnow()}')")
                    db.commit()
                    flash(f"Review added {rating}.", "success")
                    return(redirect(url_for('book', book_id=book_id)))
                     
        else:
            return(redirect(url_for('book', book_id=book_id)))
    else:
        # Make sure book exists.
        book = Book.query.get(book_id)  
        if book is None:
            return jsonify({"error": "Invalid book_id"}), 422
        else:
            reviews=db.execute(f"select r.comments, r.date_posted, r.rating, r.userid, p.username from review r, person p where r.userid=p.id and bookid = {book_id}").fetchall()
            gr_reviews=get_from_goodreads(book.isbn)
            col={}
            #work_ratings_count 
            col['work_ratings_count']=gr_reviews['books'][0]['work_ratings_count']
            #average_rating
            col['average_rating']=gr_reviews['books'][0]['average_rating']
            return render_template("book.html", book=book, reviews=reviews,gr_reviews=col)

## api access for users
@app.route("/api/books/<isbn>")
def api_query(isbn):
    if 'current_user' in session:
        # Make sure book exists.
        book = Book.query.filter_by(isbn=isbn).first()
        if book is None:
            return jsonify({"error": "Invalid ISBN number", "error_code":"422"}), 422

        # Get all passengers.
        sql = "select b.id, b.isbn, b.title, b.author, b.year, round(coalesce(avg(r.rating),0),0) rating, count(r.rating) reviews from book b "
        sql += f"left outer join review r on b.id=r.bookid where b.isbn =  '{isbn}'"
        sql += "group by b.id, b.isbn, b.title, b.author, b.year"
        
        books = db.execute(sql)
        
        for book in books:
            return jsonify({
                    "title": book.title,
                    "author": book.author,
                    "year": book.year,
                    "isbn": book.isbn,
                    "review_count": book.reviews,
                    "average_score": book.rating
                })
    else:
        flash(f"Login to extract book details", 'info')
        return redirect(url_for('login'))

# login - validates email and password
# sets session variables to track user sign in
# has remember me options to remember login info - uses cookies
@app.route("/login",  methods=['GET','POST'])
def login():
    messages={}
    #check to see if user has requested to remember previous information
    if 'email' in request.cookies:
        email = request.cookies.get('email')
        password = request.cookies.get('pwd')
    if 'current_user' in session:
        return(redirect(url_for('search'))) 
    else:
        if request.method == 'POST':
            if request.form.get("email") == '':
                messages['email']='Email cannot be empty.'
            elif validate_email(request.form.get("email")):
                email=request.form.get("email")
            else: 
                messages['email']='Invalid Email.'

            if request.form.get('password') == '':
                messages['password']='Password cannot be empty.'
            else:
                password = request.form.get("password") 
            
            if len(messages) == 0:
                user=Person.query.filter_by(email=email).first()
                rememberme=request.form.get('rememberme')
                currDate = datetime.now()

                if rememberme == 'on':
                    rememberme=True
                else:
                    rememberme=False

                if user and bcrypt.check_password_hash(user.password, password):
                    sql = f"update person set last_login='{currDate}' "
                    if user.remember != rememberme:
                        sql+= f", remember ={rememberme}"
                    #     user.remember=request.form.get('rememberme')
                    # # user.last_login = datetime.utcnow()
                    sql += f" where id={user.id}"
                    db.execute(sql)
                    db.commit() 
                    session['user_id']=user.id
                    session['current_user']=user.username
                    # messages['status']='Success!'
                    return(redirect(url_for('search'))) 
                else:
                    flash("User does not exist. Please check and retry.", "danger") 
    return render_template('login.html', title="User Login", messages=messages)

# register -  registers users
# stores hashed password
@app.route("/register",  methods=['GET','POST'])
def register():
    messages={}
    if 'current_user' in session:
        return(redirect(url_for('index'))) 
    else:
        if request.method == 'POST':
            # UI validations
            username=request.form.get("username")
            email=request.form.get("email")
            if request.form.get("username") == '':
                messages['username']='Username cannot be empty.'
            elif validate_username(request.form.get("username")):
                username=request.form.get("username") 
            else: 
                messages['username']='Invalid Username.'

            if request.form.get("email") == '':
                messages['email']='Email cannot be empty.'
            elif validate_email(request.form.get("email")):
                email=request.form.get("email") 
            else: 
                messages['email']='Invalid Email.'
            
            if request.form.get("password") == '':
                messages['password']='Password cannot be empty.'
            elif validate_password(request.form.get("password")):
                password=request.form.get("password") 
            else: 
                messages['password']='Password does not match criteria.'
            
            if request.form.get("confirmpassword") == '':
                messages['confirmpassword']='Password cannot be empty.'
            elif match_password(request.form.get("password"), request.form.get("confirmpassword")):
                confirmpassword=request.form.get("confirmpassword") 
            else: 
                messages['confirmpassword']='Passwords do not match.'
                
            if len(messages) == 0:   
                user_exists=db.execute(f"select username from person where username='{username}'").scalar()
                email_exists=db.execute(f"select email from person where email='{email}'").scalar()
                if user_exists:
                    messages['username']="User already exists."
                
                if email_exists:
                    messages['email']="Email already exists."
  
            if len(messages) > 0:
                return render_template('register.html', title="User Registration", messages=messages, email=email, username=username)
            else:
                hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
                # person = Person(username=username, email = email, password=hashed_pwd )
                # db.session.add(person)
                db.execute(f"insert into person (username, email, password) values ('{username}', '{email}', '{hashed_pwd}')")
                db.commit()
                flash(f"{username.title()}, your account is Created! Login to review books.", 'success')
                return(redirect(url_for('login')))   
    return render_template('register.html', title="User Registration", messages=messages)

# unsets session
@app.route("/logout")
def logout():
    if 'current_user' in session:
        session.pop('current_user')
    if 'user_id' in session:
        session.pop('user_id')

    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    messages={}
    if 'current_user' in session:
        return(redirect(url_for('index'))) 
    else:
        if request.method == 'POST':
            email=request.form.get("email")
            if request.form.get("email") == '':
                messages['email']='Email cannot be empty.'
            elif validate_email(request.form.get("email")):
                email=request.form.get("email") 
            else: 
                messages['email']='Invalid Email.'

            if len(messages) > 0:
                return render_template('forgot_password.html', title="Forgot Password", messages=messages)
            else:
                user = Person.query.filter_by(email=request.form.get('email')).first()
                if user:
                    send_password_reset_email(user)
                else:
                    flash(f"Invalid email. User does not exist.","danger")
                    return redirect(url_for('forgot_password'))

                flash('Check your email for the instructions to reset your password',"success")
                return redirect(url_for('login'))
    return render_template('forgot_password.html',
                           title='Forgot Password', messages=messages)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    messages={}
    if 'current_user' in session:
        return redirect(url_for('index'))
    user = Person.verify_reset_password_token(token)
    if not user:
        flash(f"Invalid email. User does not exist.","danger")
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            password=''
            if request.form.get("password") == '':
                messages['password']='Password cannot be empty.'
            elif validate_password(request.form.get("password")):
                password=request.form.get("password") 
            else: 
                messages['password']='Password does not match criteria.'
            
            if request.form.get("confirmpassword") == '':
                messages['confirmpassword']='Password cannot be empty.'
            elif match_password(password, request.form.get("confirmpassword")):
                confirmpassword=request.form.get("confirmpassword") 
            else: 
                messages['confirmpassword']='Passwords do not match.'
            if len(messages) > 0:
                return render_template('change_password.html', title="Forgot Password", messages=messages)
            else:
                hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
                db.execute(f"update Person set password='{hashed_pwd}' where id={user.id}")
                db.commit()
                flash("Password updated successfully.", "success")
                return redirect(url_for('login'))
    return render_template('change_password.html',
                           title='Change Password', messages=messages)
    

@app.route("/goodreads/get/<isbn>")
def goodreads(isbn):
    try:
        res=get_from_goodreads(isbn)
        return res
    except:
        return jsonify({"error": "Invalid book_id"}), 422
    

