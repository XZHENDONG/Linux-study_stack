# -*- coding:utf-8 -*-
import re


class VMChecker(object):
	def __init__(self, vm_instance, checker=None):
		self.vm_instance = vm_instance
		self.checker = checker
		self.result_dict = {}
	
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
				if re.search(i['stdout'], vm_stdout) and re.search(i['stderr'], vm_stderr):
					continue
				else:
					pass
		for command in self.commands_dict.iterkeys():
			if re.search(self.commands_dict[command]['stderr'], self.ssh_result[command]['stderr']) and re.search(
					self.commands_dict[command]['stdout'], self.ssh_result[command]['stdout']):
				continue
			else:
				self.checker_result[command] = {}
				self.checker_result[command]['answer'] = self.commands_dict[command]
				self.checker_result[command]['result'] = self.ssh_result[command]
		return self.checker_result


if __name__ == '__main__':
	vm_checker = SSHChecker(command_dict={'ls -al /home/asda': {'stdout': 'studenta', 'stderr': ''}})
	vm_checker.exec_check()
	result = vm_checker.check_result()
	print result
