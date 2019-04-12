# _*_ coding: utf-8 _*_
from flaskblog import app # flaskblog 파일(패키지)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)