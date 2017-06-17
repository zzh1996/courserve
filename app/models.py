from app import db
from flask_login import UserMixin
import hashlib
from datetime import datetime

Join_course = db.Table('join_course',
                       db.Column('course', db.Integer, db.ForeignKey('course.id')),
                       db.Column('student', db.Integer, db.ForeignKey('user.id'))
                       )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    role = db.Column(db.Enum('student', 'teacher', 'ta'))

    courses = db.relationship('Course', secondary=Join_course, backref='users')
    teachings = db.relationship('Course', backref='teacher_c')

    def check_password(self, password):
        s = hashlib.md5()
        s.update(password.encode('utf-8'))
        return self.password == s.hexdigest()

    def teaching(self, courseid):
        return Course.query.get(courseid).teacher == self.id

    def learning(self, courseid):
        return courseid in [c.id for c in self.courses]


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    semester = db.Column(db.String(256))
    teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    picture = db.Column(db.String(65536))

    announcements = db.relationship('Announcement')
    files = db.relationship('Course_file')
    homeworks = db.relationship('Homework')


class Course_file(db.Model):
    __tablename__ = 'course_file'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    text = db.Column(db.String(65536))
    filename = db.Column(db.String(256))


class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    text = db.Column(db.String(65536))
    time = db.Column(db.DateTime)

    def __init__(self, course, text):
        self.course = course
        self.text = text
        self.time = datetime.now()


class Homework(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    text = db.Column(db.String(65536))
    deadline = db.Column(db.DateTime)


class Homework_file(db.Model):
    __tablename__ = 'homework_file'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    student = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(256))
    time = db.Column(db.DateTime)
    grade = db.Column(db.Integer)
