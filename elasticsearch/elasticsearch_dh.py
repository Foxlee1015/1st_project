from datetime import datetime
from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from wtforms import Form, validators, SubmitField, TextAreaField, SelectField

# Flask 와 연동시 참고

es = Elasticsearch('http://localhost:9200')
app = Flask(__name__)

class Search_Form(Form):
    title = TextAreaField('Title', [validators.data_required(), validators.Length(min=1, max=20)])
    country = SelectField('Country', choices=[('US', 'US'), ('KR', 'KR'), ('JP', 'JP'), ('EP', 'EP')])
    submit = SubmitField('Request Password Reset')

@app.route('/', methods=['GET'])  # 전체 데이
def index():
    data = []
    for id in range(1,347):    ## 특허 건 수에 맞춰서 수정
        results = es.get(index='patent', doc_type='patent_test', id=id)
        data.append(results)
    return render_template('es_home.html', data=data, n = len(data))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = Search_Form(request.form)
    if request.method == "POST" :
        title, country = form.title.data, form.country.data
        print(title, country)
        result = search_data2(country, title)
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
    results = es.search(index="patent", body=body)
    re_hits = results['hits']['hits']
    n = len(re_hits)
    result = []
    for i in range(n):
        # print(re_hits[i]['_source'])
        data = re_hits[i]['_source']
        result.append([data['Country'], data['Application date'], data['Inventor'], data['title'], data['abstract'], data['Claim']])
    return result


def search_data2(keyword1, keyword2):
    body = {
        "query":  {
            "bool": {
                "must": [
                    {"match": {"Country": keyword1}},
                    {"match": {"title": keyword2}}
                    ]
                }
            },
        "size": 500 # 검색되는 건수 제한
    }
    results = es.search(index="patent", body=body)
    re_hits = results['hits']['hits']
    print(re_hits)
    n = len(re_hits)
    result = []
    for i in range(n):
        # print(re_hits[i]['_source'])
        data = re_hits[i]['_source']
        result.append([data['Country'], data['Application date'], data['Inventor'], data['title'], data['abstract'], data['Claim']])
    return result

# patent db 에서 넣기
def post_data(id, csv_data):
    doc = {}
    doc['Country'] = csv_data[0]
    doc['Document_type']= csv_data[1]
    doc['title'] = csv_data[2]
    doc['abstract'] = csv_data[3]
    doc['Claim'] = csv_data[4]
    doc['Number of claims'] = csv_data[5]
    doc['Application number'] = csv_data[6]
    doc['Application date'] = csv_data[7]
    doc['Public number'] = csv_data[8]
    doc['Public date'] = csv_data[9]
    doc['Issue number'] = csv_data[10]
    doc['Issue date'] = csv_data[11]
    doc['Inventor'] = csv_data[12]
    res = es.index(index="patent", doc_type='patent_test', id=id, body=doc)
    print(res['result'])

# 인덱스 지우기
def delete_data(index):
    res = es.indices.delete(index=index, ignore=[400, 404])

# 데이터 csv 파일 읽은 후 es post
def read_data():
    f = open('data/data2.csv', 'r', encoding='euc-kr')   # utf-8 에러 발생
    rdr = csv.reader(f)
    id = 1 # 기존 데이터 업데이트한다면 1  추가할시 기존 id 마지막 다음으로 설정 (346까지 존재)
    for line in rdr:
        if line[0] == "국가코드":   # 첫 행 무시하기
            pass
        else:
            csv_data = line
            post_data(id, csv_data)   #
            id += 1
    f.close()

if __name__ == '__main__':
    app.run(port=5000, debug=True)