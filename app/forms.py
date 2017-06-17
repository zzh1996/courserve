from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit_btn = SubmitField('登录')


class HomeworkForm(Form):
    text = StringField('作业描述', validators=[DataRequired()])
    deadline = DateField('截止日期', render_kw={"placeholder": "2000-01-01"})
    submit_btn = SubmitField('发布')
