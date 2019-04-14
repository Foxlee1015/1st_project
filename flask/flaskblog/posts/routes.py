from flask import Blueprint, render_template, url_for, flash, redirect, request, abort  # render - return 으로 해당 html 나옴 // url_for 템플릿 {{ url_for('home')}} (/home) 아님 // flash - like a popup // redirect(url_for('about') 이동
from flask_login import current_user, login_required # loginuser- db에 정보 있으면 로그인 확인 메세지/ current_user 로그 된 상태에서 -> 밑에 로그인,레지스터 눌러도 home
from flaskblog import db
from flaskblog.models import User, Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required   # 포스트하기 위해서 로그인이 필요함
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # db에 저장
        db.session.add(post)
        db.session.commit()        #post -> db 저장
        flash('Your post has been created', 'success')
        return redirect((url_for('main.home')))   # main 에 있는 home 함수 호출
    return render_template('create_post.html', title="New Post", form=form, legend='New Post')    # 실수 - form 안 넣으면 form 정의 안됨

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)         # 페이지 없으면 404 return
    return render_template('post.html', title=post.title, post=post)   # post 바로위 post 정의

@posts.route('/post/<int:post_id>/update',  methods=['GET', 'POST'])
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
        return redirect((url_for('posts.post', post_id=post_id))) # posts 의 post 호출
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content     # form 에 post 를 넣어줌.
    return render_template('create_post.html', title='update post', form=form, legend='Update Post')  # 바로위 form 을 form 으로 정의  # legend 테크,


@posts.route('/post/<int:post_id>/delete',  methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
