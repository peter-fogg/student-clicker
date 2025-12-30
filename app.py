import csv
from io import BytesIO, StringIO
import os

from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['TEMPORARY_UPLOAD_DIR'] = os.path.join(basedir, 'tempfiles')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Course(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True)
    students = db.relationship('Student', back_populates='course')
    # sections = db.relationship('Section', backref='course')


class Student(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', back_populates='students')


# class Section(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     datetime = mapped_column(DateTime)


# class Interaction(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     student = mapped_column(ForeignKey('student.id'))
#     section = mapped_column(ForeignKey('section.id'))
#     count = mapped_column(Integer)


with app.app_context():
    db.create_all() 


@app.route('/')
def index():
    courses = db.session.execute(db.select(Course)).scalars()
    return render_template('index.html', courses=courses)


@app.route('/create_class', methods=["POST"])
def create_class():
    if 'class' in request.files:
        class_name = request.form['class-name']
        course = Course(name=class_name)
        f = request.files['class']
        path = os.path.join(app.config['TEMPORARY_UPLOAD_DIR'], secure_filename(f.name))
        f.save(path)
        with open(path, 'r', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                full_name = ' '.join([row['first_name'], row['last_name']])
                student = Student(name=full_name, course=course)
                db.session.add(student)
        db.session.commit()
        os.remove(path)
    return redirect(url_for('index'))

