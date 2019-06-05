import os  #사진 파일 저장하기 위해 사진의 형식 저장
import secrets # 사진 파일 이름 바꾸기 위함
#from PIL import Image
from PIL import Image
from flask import url_for, current_app # render - return 으로 해당 html 나옴 // url_for 템플릿 {{ url_for('home')}} (/home) 아님 // flash - like a popup // redirect(url_for('about') 이동
from flaskblog import mail
from flask_mail import Message

def save_picture(form_picture):  # 첨부시 이름 상관 없이 새로운 이름으로 저장
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # 파일의 이름을 저장
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # app 패키지의 위치

    output_size = (125, 125)
    i = Image.open(form_picture)   #저장된 사진을
    i.thumbnail(output_size)      # 위 사이즈로 바꿈
    i.save(picture_path)         #   <- form_picture.save(picture_path) 원래 이렇게 저장한걸 바꿈
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreplay@demo.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no change will be made
    """
    mail.send(msg)
