# -*- coding:utf-8 -*-

import os
from datetime import datetime

import demjson
from flask import Flask, request, jsonify, url_for, Response
from flask_login import login_required, login_user
from flask_login.login_manager import LoginManager
from flask_restful import Resource, Api

from conf import config
from server.db_model import *

API_VERSION = '/api/v1'
app = Flask(__name__, static_url_path='')
app.config.from_object(config)
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


class LoginAPI(Resource):
	def post(self):
		user = User.query.filter_by(account=request.json['username']).first()
		if user and user.passwd == request.json['passwd']:
			login_user(user)
			return jsonify({'status': 1, 'message': 'welcome:' + user.username})
		return jsonify({'status': 0, 'error': '用户不存在或密码错误'})
	
	def get(self):
		return app.send_static_file('login.html')


api.add_resource(LoginAPI, API_VERSION + '/login/', '/login/')


class Practice(Resource):
	def get(self):
		page = int(request.args.get('table_rows')) / 10 + 1
		result = Exercise.query.paginate(page, per_page=10)
		return page
	
	def post(self):
		markdown = request.json['markdown']
		markdown = markdown.split('```json')
		markdown[0] = ''.join(markdown[0:-1])
		html = request.json['html']
		html = html.split('<pre><code class="lang-json">')
		title_html = ''.join(html[0:-1])
		title = markdown[0].strip()
		checker_json = markdown[-1].strip('```')
		checker_dict = demjson.decode(checker_json, encoding='utf8')
		exerc = Exercise(title=title, title_html=title_html)
		db.session.add(exerc)
		db.session.commit()
		for checker in checker_dict['checker']:
			try:
				checker = Checker(execID=exerc.ID,
				                  title=checker['title'],
				                  command=checker['command'],
				                  stdout=checker['stdout'],
				                  stderr=checker['stderr'],
				                  score=checker['score'])
				db.session.add(checker)
				db.session.commit()
				return {"status": 1, "message": exerc.ID}
			except Exception as e:
				return {"status": 0, "error": e}


api.add_resource(Practice, API_VERSION + '/practices')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
	return app.send_static_file('index.html')


@app.route('/editor/', methods=['GET', 'POST'])
@login_required
def editor():
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
