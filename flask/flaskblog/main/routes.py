from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=3)   # db 에서 한 페이지에 5개만 // .order_by(Post.date.desc()) - 포스트 순서 시간기준 오래된것 앞으로
    return render_template('home.html', posts=posts)  # 앞 posts 는 home.html 에서 오고, 뒤는 위에 post 정보(hello.py 내부)

@main.route('/about')
def about():
    return render_template('about.html', title="about")  # title 제공 - about.html 의 if 확인

@main.route('/patent')
def patent():
    return render_template('patent.html', title="Patent")
