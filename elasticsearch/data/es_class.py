import csv
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

class Data_handler():
    def __init__(self,filename,index, doc_type):
        self.filename=filename
        self.index=index
        self.doc_type=doc_type

    # 파일 업로드
    def upload_data(self):
        filename, index, doc_type = self.filename, self.index, self.doc_type
        f = open('data/{0}.csv'.format(filename), 'r', encoding='utf-8')  # utf-8 에러 발생 // euc-kr
        rdr = csv.reader(f)
        id = 1  # 기존 데이터 업데이트한다면 1  추가할시 기존 id 마지막 다음으로 설정 (346까지 존재)
        for line in rdr:
            try:
                if schema:          # 첫 행 스키마
                    csv_data = line
                    doc = {}
                    for i in range(len(schema)):
                        if not csv_data[i]:
                            csv_data= " "
                        doc[schema[i]] = csv_data[i]
                    res = es.index(index=index, doc_type=doc_type, id=id, body=doc)
                    print(id, res)
                    id += 1
            except:
                schema = line       # \ufeff 국가코드 앞에 생김 확인 필요.
        f.close()

class Index_handler():
    def __init__(self, index):
        self.index=index

    def delete(self):
        index=self.index
        res = es.indices.delete(index=index, ignore=[400, 404])