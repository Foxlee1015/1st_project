# _*_ coding: utf-8 _*_
from flask import Flask, render_template, url_for

app = Flask(__name__)

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
    return render_template('home.html', posts=posts)  # 앞 posts 는 home.html 에서 오고, 뒤는 위에 post 정보

@app.route('/about')
def about():
    return render_template('about.html', title="About")  # title 제공

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)