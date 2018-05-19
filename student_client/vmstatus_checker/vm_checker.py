# -*- coding:utf-8 -*-
import re


class VMChecker(object):
	def __init__(self, vm_instance, checker=None):
		self.vm_instance = vm_instance
		self.checker = checker
		self.result_dict = {}
		self.checker_result={}
		self.checker_result['failID']=[]
	
	def exec_check(self):
		with self.vm_instance.create_session() as session:
			with session.console.guest.create_session('root', '123456')as gs:
				for i in self.checker:
					process, stdout, stderr = gs.execute('/bin/bash', ['-c', i['command']])
					self.result_dict[i['command']] = {}
					self.result_dict[i['command']]['stdout'] = stdout
					self.result_dict[i['command']]['stderr'] = stderr
	
	def check_result(self):
		if self.result_dict:
			self.exec_check()
		else:
			for i in self.checker:
				vm_stdout = self.result_dict[i['command']]['stdout']
				vm_stderr = self.result_dict[i['command']]['stderr']
				self.checker_result[self.checker['id']] = {}
				self.checker_result[self.checker['id']]['stdout'] = vm_stdout
				self.checker_result[self.checker['id']]['stderr'] = vm_stderr
				if re.search(i['stdout'], vm_stdout) and re.search(i['stderr'], vm_stderr):
					continue
				else:
					self.checker_result['failID'].append(self.checker['id'])
	

