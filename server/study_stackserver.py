# -*- coding:utf-8 -*-

import os
from datetime import datetime

import demjson
from flask import Flask, request, jsonify, url_for, Response, render_template
from flask_login import login_required, login_user
from flask_login.login_manager import LoginManager
from flask_restful import Resource, Api

from conf import config
from server.db_model import *

API_VERSION = '/api/v1'
app = Flask(__name__, static_url_path='')
app.config.from_object(config)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)
login_manager = LoginManager()
login_manager.login_view = '/login/'
login_manager.session_protection = 'strong'
login_manager.init_app(app)
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	user_account = User.query.filter_by(account=user_id).first()
	return user_account


class CheckerResultAPI(Resource):
	def get(self):
		pass
	
	def put(self):
		pass


class LoginAPI(Resource):
	def post(self):
		account = request.json['account']
		user = User.query.filter_by(account=account).first()
		if user and user.passwd == request.json['passwd'] and user.role in [request.json['role'], 'admin']:
			login_user(user)
			return jsonify({'status': 1, 'message': user.username, 'user_id': user.ID})
		return jsonify({'status': 0, 'error': '用户不存在或密码错误'})
	
	def get(self):
		return app.send_static_file('login.html')


api.add_resource(LoginAPI, API_VERSION + '/login/', '/login/')


class RegisterAPI(Resource):
	def post(self):
		user = User.query.filter_by(account=request.json['account']).first()
		if not user:
			user = User(username=request.json['username'],
			            passwd=request.json['passwd'],
			            account=request.json['account'],
			            role=request.json['role'])
			db.session.add(user)
			try:
				db.session.commit()
			except Exception as e:
				return {"status": 0, "error": e}
		else:
			return {"status": 0, "error": "账号已存在"}
		return {"status": 1, "message": '用户创建成功', "user_id": user.ID}


api.add_resource(RegisterAPI, API_VERSION + '/register/')


class PracticeAPI(Resource):
	def get(self):
		# page = int(request.args.get('table_rows')) / 10 + 1
		if request.args.get('exerc_id'):
			result = Checker.query.filter_by(exercID=request.args.get('exerc_id')).all()
			if result:
				respone = {}
				respone['exerc_markdown'] = result[0].exercise.title
				respone['exerc_html'] = result[0].exercise.title_html
				respone['checker'] = []
				for i in result:
					check_dict = {}
					check_dict['ID'] = i.ID
					check_dict['title'] = i.title
					check_dict['command'] = i.command
					check_dict['stdout'] = i.stdout
					check_dict['stderr'] = i.stderr
					check_dict['score'] = i.score
					respone['checker'].append(check_dict)
				return respone
			return
		if request.args.get('table_rows'):
			page = int(request.args.get('table_rows')) + 1
			result = Exercise.query.paginate(page, per_page=10)
			respone = {}
			respone['next'] = result.has_next
			respone['next_page'] = result.page + 1
			respone['exerc'] = []
			respone['exerc'] = []
			for i in result.items:
				exerc_dict = {}
				exerc_dict['exerc_id'] = i.ID
				exerc_dict['exerc_markdown'] = i.title
				exerc_dict['exerc_html'] = i.title_html
				respone['exerc'].append(exerc_dict)
			return respone
	
	def post(self):
		markdown = request.json['markdown']
		markdown = markdown.split('```json')
		checker_json = markdown[-1].strip('```')
		checker_dict = demjson.decode(checker_json, encoding='utf8')
		exerc = Exercise(title=request.json['markdown'], title_html=request.json['html'])
		db.session.add(exerc)
		db.session.commit()
		try:
			for checker in checker_dict['checker']:
				checker = Checker(exercID=exerc.ID,
				                  title=checker['title'],
				                  command=checker['command'],
				                  stdout=checker['stdout'],
				                  stderr=checker['stderr'],
				                  score=checker['score'])
				db.session.add(checker)
			db.session.commit()
		except Exception as e:
			return {"status": 0, "error": e}
		return {"status": 1, "message": '题目创建成功', "exerc_id": exerc.ID}
	
	def put(self):
		markdown = request.json['markdown']
		markdown = markdown.split('```json')
		checker_json = markdown[-1].strip('```')
		checker_dict = demjson.decode(checker_json, encoding='utf8')
		checker_list = checker_dict['checker']
		try:
			result = Exercise.query.get(request.json['exerc_id'])
			result.title = request.json['markdown']
			result.title_html = request.json['html']
			check_result = Checker.query.filter_by(exercID=request.json['exerc_id']).all()
			for i in xrange(len(check_result)):
				if i > len(checker_list):
					user_result = CheckResult.query.filter_by(checkerID=check_result[i].ID).all()
					for result in user_result:
						db.session.delete(result)
					db.session.delete(check_result[i])
				else:
					check_result[i].exercID = request.json['exerc_id']
					check_result[i].title = checker_list[i]['title']
					check_result[i].command = checker_list[i]['command']
					check_result[i].stdout = checker_list[i]['stdout']
					check_result[i].stderr = checker_list[i]['stderr']
					check_result[i].score = checker_list[i]['score']
					del checker_list[i]
			if checker_list:
				for checker in checker_list:
					checker = Checker(exercID=request.json['exerc_id'],
					                  title=checker['title'],
					                  command=checker['command'],
					                  stdout=checker['stdout'],
					                  stderr=checker['stderr'],
					                  score=checker['score'])
					db.session.add(checker)
			db.session.commit()
		except Exception as e:
			return {'status': 0, 'error': e}
		return {'status': 1, 'message': '保存成功'}
	
	def delete(self):
		print request.json
		try:
			result = Checker.query.filter_by(exercID=int(request.json['delete_id'])).all()
			for i in result:
				db.session.delete(i)
			db.session.delete(result[0].exercise)
			db.session.commit()
			return {'status': 1, 'message': '删除成功'}
		except Exception as e:
			return {'status': 0, 'error': e}


api.add_resource(PracticeAPI, API_VERSION + '/practices')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
	return app.send_static_file('index.html')


@app.route('/editor/', methods=['GET'])
@login_required
def editor():
	if request.args.get('exerc_id'):
		result = Checker.query.filter_by(exercID=request.args.get('exerc_id')).all()
		return render_template('editor.html', exerc_id=result[0].exercise.ID, exerc=result[0].exercise.title)
	return app.send_static_file('editor.html')


@app.route('/student_status/', methods=['GET'])
@login_required
def student_status():
	return app.send_static_file('student_status.html')


@app.route('/upload/', methods=['POST'])
@login_required
def upload():
	file = request.files.get('editormd-image-file')
	if not file:
		res = {
			'success': 0,
			'message': u'图片格式异常'
		}
	else:
		ex = os.path.splitext(file.filename)[1]
		filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
		file.save(os.path.join(app.config['SAVEPIC'], filename))
		# 返回
		res = {
			'success': 1,
			'message': u'图片上传成功',
			'url': url_for('.image', name=filename)
		}
	return jsonify(res)


# 编辑器上传图片处理
@app.route('/image/<name>')
@login_required
def image(name):
	with open(os.path.join(app.config['SAVEPIC'], name), 'rb') as f:
		resp = Response(f.read(), mimetype="image/jpeg")
	return resp


if __name__ == '__main__':
	app.run(host=app.config['LISTEN_HOST'], port=app.config['PORT'], debug=True)
