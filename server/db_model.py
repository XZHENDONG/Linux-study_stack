# -*- coding:utf-8 -*-
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Checker(db.Model):
	__tablename__ = 'checker'
	
	ID = db.Column(db.Integer, primary_key=True)
	exercID = db.Column(db.ForeignKey(u'exercises.ID'), index=True)
	title = db.Column(db.Text, nullable=False)
	command = db.Column(db.Text, nullable=False)
	stdout = db.Column(db.Text, nullable=False)
	stderr = db.Column(db.Text, nullable=False)
	score = db.Column(db.Integer, nullable=False)
	
	exercise = db.relationship(u'Exercise')


class Exercise(db.Model):
	__tablename__ = 'exercises'
	
	ID = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text, nullable=False)
	title_html = db.Column(db.Text, nullable=False)


class User(UserMixin, db.Model):
	__tablename__ = 'user'
	
	ID = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30))
	passwd = db.Column(db.String(128))
	role = db.Column(db.Enum(u'admin', u'student', u'teacher'))
	account = db.Column(db.String(45), unique=True)
	
	def get_id(self):
		return self.account


class CheckResult(db.Model):
	__tablename__ = 'check_result'
	
	userID = db.Column(db.ForeignKey(u'user.ID'), primary_key=True, nullable=False)
	checkerID = db.Column(db.ForeignKey(u'checker.ID'), primary_key=True, nullable=False, index=True)
	stdout = db.Column(db.String)
	stderr = db.Column(db.String)
	status = db.Column(db.Integer)
	time = db.Column(db.DateTime, nullable=False,
	                 server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
	
	checker = db.relationship(u'Checker')
	user = db.relationship(u'User')
