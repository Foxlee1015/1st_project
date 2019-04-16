from flask import render_template, url_for, flash, redirect, request, Blueprint  # render - return 으로 해당 html 나옴 // url_for 템플릿 {{ url_for('home')}} (/home) 아님 // flash - like a popup // redirect(url_for('about') 이동
from flaskblog import db, bcrypt
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required # loginuser- db에 정보 있으면 로그인 확인 메세지/ current_user 로그 된 상태에서 -> 밑에 로그인,레지스터 눌러도 home
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:                  # 로그인한 상태라면
        return redirect(url_for('main.home'))
    form = RegistrationForm()    # forms.py 의 form
    if form.validate_on_submit():   # form 이 정상적으로 제출되면
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        # 커맨드에서 로그인 설정
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) # 비밀번호
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login')) # home 함수
    return render_template('register.html', title="Register", form=form)  # title 제공


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:    # 로그인한 상태라면
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():  # form.validate_on_submit 은 어디서 호출??
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page =request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title="Login", form=form)  # title 제공

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)   # 위에서 정의한 함수 savepicture 에 form 에 올라온 사진 넣음음            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', "success")
        return redirect(url_for('users.account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)



@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=3)   # db 에서 한 페이지에 5개만 // .order_by(Post.date.desc()) - 포스트 순서 시간기준 오래된것 앞으로
    return render_template('user_posts.html', posts=posts, user=user)  # 앞 posts 는 home.html 에서 오고, 뒤는 위에 post 정보(hello.py 내부)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:    # 로그인된 상태라면 홈으로 로그아웃
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:    # 로그인된 상태라면 홈으로 로그아웃
        return redirect(url_for('main.home'))
    user =User.verity_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')   # warning - yellow outline
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():   # use 정보 이미 있음
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        # 커맨드에서 로그인 설정
        user.password = hashed_password  # 비밀번호 업뎃이트
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login')) # home 함수
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route('/patent/register')
def patent_reg():
    return render_template(('patent_reg.html'))