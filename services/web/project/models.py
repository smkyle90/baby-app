from datetime import datetime

from flask_login import UserMixin

from . import db


class Patient(UserMixin, db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000), unique=True)
    exams = db.relationship("Exam", backref="patient", lazy=True)
    notes = db.relationship("Note", backref="patient", lazy=True)
    password = db.Column(db.String(100))
    no_pregnancies = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    weight = db.Column(db.Integer, default=0)
    in_labour = db.Column(db.Float, default=0)
    profile_init = db.Column(db.Boolean, default=False)
    email_confirmed = db.Column(db.Boolean, default=False)

class Exam(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), db.ForeignKey("patient.name"), nullable=False)
    dilation = db.Column(db.Integer, default=0)
    effacement = db.Column(db.Integer, default=0)
    station = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Note(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), db.ForeignKey("patient.name"), nullable=False)
    note = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

# def init_db():
#     db.create_all()

# if __name__ == '__main__':
#     init_db()
