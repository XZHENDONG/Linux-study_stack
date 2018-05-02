# -*- coding:utf-8 -*-
from flask_login import UserMixin
from flask_restful import fields
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Checker(db.Model):
	__tablename__ = 'checker'
	
	ID = db.Column(db.Integer, primary_key=True)
	execID = db.Column(db.ForeignKey(u'exercises.ID'), index=True)
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
	author = db.Column(db.String(20))


class User(UserMixin, db.Model):
	__tablename__ = 'user'
	
	ID = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30))
	passwd = db.Column(db.String(128))
	role = db.Column(db.Integer)
	account = db.Column(db.String(45), unique=True)
	_class = db.Column('class', db.String(45))
	
	def get_id(self):
		return self.account
	


class UserResult(db.Model):
	__tablename__ = 'user_result'
	__table_args__ = (
		db.Index('userID_checkerID_index', 'userID', 'checkerID'),
	)
	
	ID = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.ForeignKey(u'user.ID'))
	checkerID = db.Column(db.ForeignKey(u'checker.ID'), index=True)
	stdin = db.Column(db.String)
	stderr = db.Column(db.String)
	time = db.Column(db.DateTime, nullable=False,
	                 server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
	
	checker = db.relationship(u'Checker')
	user = db.relationship(u'User')


checker_fields = {
	'ID': fields.Integer,
	'execID': fields.Integer,
	'title': fields.String,
	'command': fields.String,
	'stdout': fields.String,
	'stderr': fields.String,
	'score': fields.Integer,
}

exec_fields = {
	'ID': fields.Integer,
	'title': fields.String,
	'author': fields.String
}

user_fields = {
	'ID': fields.Integer,
	'username': fields.String,
	'passwd': fields.String,
	'role': fields.Integer,
	'account': fields.String,
	'class': fields.String
}

user_result_fields = {
	'ID': fields.Integer,
	'userID': fields.Integer,
	'checkerID': fields.Integer,
	'stdin': fields.String,
	'stderr': fields.String,
	'status': fields.Integer,
	'time': fields.DateTime
}
