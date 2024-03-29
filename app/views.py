from flask import render_template, redirect, url_for, request, flash, abort, send_file
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.models import *
from app.forms import *


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role == 'student':
        courses = current_user.courses
    elif current_user.role == 'teacher':
        courses = current_user.teachings
    return render_template('index.html', user=current_user, courses=courses, active=1)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form['email'].data
            password = form['password'].data
            user = User.query.filter_by(email=email).first()
            if not user:
                flash('Email not found', 'error')
            elif not user.check_password(password):
                flash('Email or password incorrect', 'error')
            else:
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/search/')
@login_required
def search():
    courses = Course.query.filter(Course.name.like('%' + request.args.get('s') + '%')).all()
    return render_template('search.html', user=current_user, courses=courses, active=0, s=request.args.get('s'))


@app.route('/course/<int:id>/')
@login_required
def course(id):
    return redirect(url_for('announcement', id=id))


@app.route('/course/<int:id>/announcement/', methods=['POST', 'GET'])
@login_required
def announcement(id):
    if request.method == 'POST':
        if current_user.teaching(id):
            text = request.form['text']
            a = Announcement(id, text)
            db.session.add(a)
            db.session.commit()
            return redirect(url_for('announcement', id=id))
    c = Course.query.get(id)
    a = c.announcements
    return render_template('announcement.html', user=current_user, course=c, announcements=a,
                           active=2, admin=current_user.role == 'teacher')


@app.route('/course/<int:id>/announcement_delete/<int:aid>')
@login_required
def announcement_delete(id, aid):
    a = Announcement.query.get(aid)
    if current_user.teaching(a.course):
        db.session.delete(a)
        db.session.commit()
    return redirect(url_for('announcement', id=id))


@app.route('/course/<int:id>/file/', methods=['POST', 'GET'])
@login_required
def file(id):
    if request.method == 'POST':
        if current_user.teaching(id):
            file = request.files['file']
            f = Course_file(id, file)
            db.session.add(f)
            db.session.commit()
            return redirect(url_for('file', id=id))
    c = Course.query.get(id)
    f = c.files
    return render_template('file.html', user=current_user, course=c, files=f,
                           active=2, admin=current_user.role == 'teacher')


@app.route('/download/<int:id>/')
@login_required
def download(id):
    f = Course_file.query.get(id)
    return send_file(app.config['UPLOAD_FOLDER'] + f.filename, as_attachment=True, attachment_filename=f.text)


@app.route('/course/<int:id>/file_delete/<int:fid>')
@login_required
def file_delete(id, fid):
    f = Course_file.query.get(fid)
    if current_user.teaching(f.course):
        db.session.delete(f)
        db.session.commit()
    return redirect(url_for('file', id=id))


@app.route('/course/<int:id>/homework/', methods=['POST', 'GET'])
@login_required
def homework(id):
    form = HomeworkForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit() and current_user.teaching(id):
            text = form['text'].data
            deadline = form['deadline'].data
            h = Homework(id, text, deadline)
            db.session.add(h)
            db.session.commit()
            return redirect(url_for('homework', id=id))
    c = Course.query.get(id)
    h = c.homeworks
    return render_template('homework.html', user=current_user, course=c, homeworks=h,
                           active=2, admin=current_user.role == 'teacher', form=form)


@app.route('/course/<int:id>/homework_delete/<int:hid>')
@login_required
def homework_delete(id, hid):
    h = Homework.query.get(hid)
    if current_user.teaching(h.course):
        db.session.delete(h)
        db.session.commit()
    return redirect(url_for('homework', id=id))


@app.route('/course/<int:id>/list/')
@login_required
def list(id):
    c = Course.query.get(id)
    return render_template('list.html', user=current_user, course=c, students=c.students,
                           active=2, admin=current_user.role == 'teacher')


@app.route('/news/')
@login_required
def news():
    pass
