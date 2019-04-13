from flask import render_template, url_for, flash, redirect, request  # render - return 으로 해당 html 나옴 // url_for 템플릿 {{ url_for('home')}} (/home) 아님 // flash - like a popup // redirect(url_for('about') 이동
from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm # 내가 만든 forms.py 정의한 함수(RegistrationForm, LoginForm) import
from flaskblog.models import User, Post
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required # loginuser- db에 정보 있으면 로그인 확인 메세지/ current_user 로그 된 상태에서 -> 밑에 로그인,레지스터 눌러도 home

bcrypt = Bcrypt(app)

posts = [
    {
        'author' : 'Daehan',
        'title' : 'Post 1',
        'content' : '1st',
        'date' : '20190410'
    },
    {
        'author': 'Fox',
        'title': 'Post 2',
        'content': '2nd',
        'date': '20190411'
    }
]

@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html', posts=posts)  # 앞 posts 는 home.html 에서 오고, 뒤는 위에 post 정보(hello.py 내부)

@app.route('/about')
def about():
    return render_template('about.html', title="About")  # title 제공 - about.html 의 if 확인

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:                  # 로그인한 상태라면
        return redirect(url_for('home'))
    form = RegistrationForm()    # forms.py 의 form
    if form.validate_on_submit():   # form 이 정상적으로 제출되면
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        # 커맨드에서 로그인 설정
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) # 비밀번호
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login')) # home 함수
    return render_template('register.html', title="Register", form=form)  # title 제공


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:    # 로그인한 상태라면
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():  # form.validate_on_submit 은 어디서 호출??
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page =request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title="Login", form=form)  # title 제공

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account',  methods=['GET', 'POST'])
@login_required # 데코
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', "success")
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)

@app.route('/patent')
def patent():
    return render_template('patent.html', title="Patent")