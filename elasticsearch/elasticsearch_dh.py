from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from wtforms import Form, validators, SubmitField, TextAreaField, SelectField
from data.es_class import Data_handler   # data = 디렉토리, es_class = 파일명(py), Data_handler = 클래스

es = Elasticsearch('http://localhost:9200')
app = Flask(__name__)

class Search_Form(Form):
    title = TextAreaField('Title', [validators.data_required(), validators.Length(min=1, max=20)])
    abstract = TextAreaField('Title', [validators.data_required(), validators.Length(min=1, max=20)])
    country = SelectField('Country', choices=[('US', 'US'), ('KR', 'KR'), ('JP', 'JP'), ('EP', 'EP')])
    submit = SubmitField('Request Password Reset')

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

"""
csv 파일 확인사항  // filename=index (대문자 X) // "," 제거  // 빈칸 채우기  // column 확인 // 지울때는 doc_type 무시가능
인코딩 에러시 euc-kr 또는 utf-8-sig 둘 중 하나 사용
"""
#data=Data_handler("index","doc_type")
#data=Data_handler("egr", "patent")
#data.upload_data()
#data.delete_index()

if __name__ == '__main__':
    app.run(port=5000, debug=True)