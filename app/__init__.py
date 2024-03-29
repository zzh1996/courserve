#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://courserve:courserve@localhost/courserve?charset=utf8'
app.config['SECRET_KEY'] = 'key'
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/uploads/'
db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import *


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


from app.views import *
