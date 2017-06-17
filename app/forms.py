from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = StringField('密码', validators=[DataRequired()])
    submit_btn = SubmitField('登录')