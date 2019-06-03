from elasticsearch import Elasticsearch
import csv
#from flask import jsonify

# When Elasticsearch is running
es = Elasticsearch('http://localhost:9200')

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

def delete_data(index):
    res = es.indices.delete(index=index, ignore=[400, 404])

def read_data():
    f = open('data/data2.csv', 'r', encoding='euc-kr')   # utf-8 에러 발생
    rdr = csv.reader(f)
    id = 1 # id 설정
    for line in rdr:
        if line[0] == "국가코드":   # 첫 행 무시하기
            pass
        else:
            csv_data = line
            post_data(id, csv_data)
            id += 1
    f.close()

def search_data(keyword):
    body = {
        "query": {
            "match": {                    # "multi_match"
                "Country": keyword
            }
        }
    }
    res = es.search(index="patent", body=body)  # doc_type="patent_test" 있으면 에러 뜸
    print((res['hits']['hits']))

def search_multi_data(keyword1, keyword2):
    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"Country": keyword1}},
                    {"match": {"Inventor": keyword2}}
                    ]
                }
            }
        }
    res = es.search(index="patent", body=body)  # doc_type="patent_test" 있으면 에러 뜸
    x = res['hits']['hits']
    for i in range(len(x)):
        print(x[i])
    #print((res['hits']['hits']))

# size(출력되는 id의 갯수, 기본 size 는 10) 변경은 Insomina 에서 GET http://127.0.0.1:9200/patent/patent_test/_search
# {
#   "query": { "match_all": {} },
#   "size": 20
# }

#read_data()   # id 먼저 확인, update or create ?
#delete_data("patent")
search_data("KR")
#search_multi_data("JP","NGK SPARK PLUG CO LTD")