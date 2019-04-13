import os  #사진 파일 저장하기 위해 사진의 형식 저장
import secrets # 사진 파일 이름 바꾸기 위함
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort  # render - return 으로 해당 html 나옴 // url_for 템플릿 {{ url_for('home')}} (/home) 아님 // flash - like a popup // redirect(url_for('about') 이동
from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required # loginuser- db에 정보 있으면 로그인 확인 메세지/ current_user 로그 된 상태에서 -> 밑에 로그인,레지스터 눌러도 home

bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()   # db 에서 post 모두 가져와라
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

def save_picture(form_picture):  # 첨부시 이름 상관 없이 새로운 이름으로 저장
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # 파일의 이름을 저장
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # app 패키지의 위치

    output_size = (125, 125)
    i = Image.open(form_picture)   #저장된 사진을
    i.thumbnail(output_size)      # 위 사이즈로 바꿈
    i.save(picture_path)         #   <- form_picture.save(picture_path) 원래 이렇게 저장한걸 바꿈
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)

@app.route('/patent')
def patent():
    return render_template('patent.html', title="Patent")

@app.route('/post/new', methods=['GET', 'POST'])
@login_required   # 포스트하기 위해서 로그인이 필요함
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # db에 저장
        db.session.add(post)
        db.session.commit()        #post -> db 저장
        flash('Your post has been created', 'success')
        return redirect((url_for('home')))
    return render_template('create_post.html', title="New Post", form=form, legend='New Post')    # 실수 - form 안 넣으면 form 정의 안됨

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)         # 페이지 없으면 404 return
    return render_template('post.html', title=post.title, post=post)   # post 바로위 post 정의

@app.route('/post/<int:post_id>/update',  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)                    # 작성자가 다르면 접근불가 from flask
    form = PostForm()
    if form.validate_on_submit():             # 업데이트 위해 새로 작성된 post 가 submit 되면
        post.title = form.title.data          # post 로 title, content 가 저장되고
        post.content = form.content.data
        db.session.commit()                  # 이미 db 에 있기 때문에 add 필요 없음
        flash('Your post has been updated!', 'success')
        return redirect((url_for('post', post_id=post_id)))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content     # form 에 post 를 넣어줌.
    return render_template('create_post.html', title='update post', form=form, legend='Update Post')  # 바로위 form 을 form 으로 정의  # legend 테크,


@app.route('/post/<int:post_id>/delete',  methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))