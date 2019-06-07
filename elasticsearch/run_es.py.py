import os
from flask import Flask, request, render_template, flash, url_for, redirect
from elasticsearch import Elasticsearch
from data.es_class import Data_handler   # data = 디렉토리, es_class = 파일명(py), Data_handler = 클래스
from forms.form import Search_Form, File_Form, Submit_Form
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'data/'

es = Elasticsearch('http://localhost:9200')
app = Flask(__name__)
app.jinja_env.auto_reload= True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# 현재 저장된 인덱스 리스트 출력
@app.route('/', methods=['GET'])
def home():
    index_data = []
    for index in es.indices.get_alias("*"):
        index_data.append(index)
    return render_template('es_home.html', data=index_data, n=len(index_data))

# 특정 인덱스만 출력
@app.route('/index/<string:index>/size/<int:number>', methods=['GET', 'POST'])
def index(index,number):
    data = []
    for id in range(1,number):
        results = es.get(index=index, doc_type="patent", id=id)
        data.append(results)
    if request.method == "POST" :
        data=Data_handler(index,"patent")
        data.delete_index()
        return redirect(url_for('home'))
    else:
        return render_template('es_index.html', data=data, n = len(data))

@app.route('/search/<string:index>', methods=['GET', 'POST'])
def search(index):
    form = Search_Form(request.form)
    if request.method == "POST" :
        title, country, abstract = form.title.data, form.country.data, form.abstract.data
        data = Data_handler(index, "patent")                   # DOC_TYPE 추후 수정 필요
        result = data.search_data(country, title, abstract)
        return render_template('es_search.html', results=result, n=len(result), form=form)
    else:
        return render_template('es_search.html', results=None, form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = File_Form(request.form)
    if request.method == "POST":
        file = request.files['file']
        if not file or file.filename == "":
            flash('파일을 확인해주세요.')
            return render_template("db_register.html", form=form)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data=Data_handler(filename[:-4], "patent")
            data.upload_data()
            flash(file.filename)
            flash('등록되었습니다.')
            return render_template('db_register.html', form=form)
    else:
        flash('파일을 등록해주십시오')
        return render_template('db_register.html', form=form)

if __name__ == '__main__':
    app.run(port=5000, debug=True)