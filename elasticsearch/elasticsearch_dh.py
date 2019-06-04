from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from wtforms import Form, validators, SubmitField, TextAreaField, SelectField
import csv
from data.es_class import Data_handler   # data = 디렉토리, es_class = 파일명(py), Data_handler = 클래스
from data.es_class import Index_handler

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
        result = search_data2(index, country, title, abstract)
        return render_template('es_search.html', results=result, n=len(result), form=form)
    else:
        return render_template('es_search.html', results=None, form=form)

def search_data1(keyword):
    body = {
        "query": {
            "match": {
                "Country": keyword
            }
        },
        "size": 500 # 검색되는 건수 제한
    }
    results = es.search(index="nisshin", body=body)
    re_hits = results['hits']['hits']
    n = len(re_hits)
    result = []
    for i in range(n):
        # print(re_hits[i]['_source'])
        data = re_hits[i]['_source']
        result.append([data['Country'], data['Application date'], data['Inventor'], data['Title'], data['Abstract'], data['Claim']])
    return result

def search_data2(index, keyword1, keyword2, keyword3):
    body = {
        "query":  {
            "bool": {
                "should": [
                    {"match": {"\ufeff국가코드": keyword1}},
                    {"match": {"발명의 명칭": keyword2}},
                    {"match": {"요약": keyword3}}
                    ]
                }
            },
        "size": 500 # 검색되는 건수 제한
    }
    results = es.search(index=index, body=body)
    re_hits = results['hits']['hits']
    n = len(re_hits)
    result = []
    for i in range(n):
        data = re_hits[i]['_source']
        result.append([data['\ufeff국가코드'], data['출원일'], data['출원인'], data['발명의 명칭'], data['요약'], data['대표청구항']])
    return result

# csv 파일 확인사항 1. , 제거 2. 빈칸 채우기 3. column 확인
#add_data1 = Data_handler("filename", "index", "doc_type")
#add_data1.upload_data()

#delete_index = Index_handler("index")
#delete_index.delete()


if __name__ == '__main__':
    app.run(port=5000, debug=True)