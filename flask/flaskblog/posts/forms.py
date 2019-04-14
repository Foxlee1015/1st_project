from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField  # 포스트 내용에 넣기위함 textareafield
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
