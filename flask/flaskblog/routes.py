from flask import render_template, url_for, flash, redirect  # render - return 으로 해당 html 나옴 // url_for 템플릿 {{ url_for('home')}} (/home) 아님 // flash - like a popup // redirect(url_for('about') 이동
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm  # 내가 만든 forms.py 정의한 함수(RegistrationForm, LoginForm) import
from flaskblog.models import User, Post

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
    form = RegistrationForm()    # forms.py 의 form
    if form.validate_on_submit():   # form 이 정상적으로 제출되면
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # home 함수
    return render_template('register.html', title="Register", form=form)  # title 제공


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # form.validate_on_submit 은 어디서 호출??
        if form.email.data == 'admin@blog.com' and form.password.data =="password":
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=form)  # title 제공
