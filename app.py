import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
print(app.config['SQLALCHEMY_DATABASE_URI'])
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Student(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)


class Course(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True)
    students = db.relationship('Student', backref='course')
    sections = db.relationship('Section', backref='course')


class Section(db.Model):
    id = mapped_column(Integer, primary_key=True)
    datetime = mapped_column(DateTime)


class Interaction(db.Model):
    id = mapped_column(Interaction, primary_key=True)
    student = mapped_column(ForeignKey('student.id'))
    section = mapped_column(ForeignKey('section.id'))
    count = mapped_column(Integer)


with app.app_context():
    db.create_all() 


@app.route('/')
def index():
    return 'hi there'


