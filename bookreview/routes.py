from datetime import datetime

from flask import request, render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from bookreview import app, db, con, bcrypt
from bookreview.models import Book, Person, Review
from bookreview.forms import RegistrationForm, LoginForm, UpdateAccountForm, SearchForm

@app.route("/", methods=['GET','POST'])
def index():
    form=SearchForm()
    if form.validate_on_submit():
        option=form.select.data
        text=form.search.data
        result=con.execute(f"select * from book where {option} ilike '%{text}%'")
        #print(f"select * from book where lower({option}) like '%{text.lower()}%'")
        return render_template('index.html', title="Search for Books", form=form, results=result)
    return render_template('index.html', title="Search for Books", form=form)

@app.route("/about")
def about():
    return render_template('about.html', title="The About Page")

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return(redirect(url_for('index')))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=form.username.data
        email=form.email.data
        person = Person(username=user, email = email, password=hashed_pwd )
        db.session.add(person)
        db.session.commit()
        flash(f'Your account is Created! Login to review books.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="User Registration", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return(redirect(url_for('index')))  
    form=LoginForm()
    if form.validate_on_submit():
        user = Person.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            user.remember = form.remember.data
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Incorrect Email or Password.', 'danger')
    return render_template('login.html', title="User Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account",  methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account details updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    #image_file=url_for('static',filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title="User Account", form=form)


    @app.route("/reset", methods=['GET','POST'])
def reset():
    if current_user.is_authenticated:
        return(redirect(url_for('index')))  
    form=ResetForm()
    if form.validate_on_submit():
        user = Person.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            user.remember = form.remember.data
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Incorrect Email or Password.', 'danger')
    return render_template('login.html', title="User Login", form=form)