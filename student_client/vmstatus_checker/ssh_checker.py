# -*- coding:utf-8 -*-
import re

import paramiko

from student_client.vmstatus_checker import vm_control


class SSHChecker(object):
	def __init__(self, ssh_port=22, command_dict=None):
		self._ssh_client = None
		self._vm = vm_control.StackVM()
		self.vm_ip = self._vm.get_ip()
		self.ssh_port = ssh_port
		self.ssh_result = {}
		self.commands_dict = command_dict
		self.checker_result = {}
	
	def exec_check(self):
		self._ssh_client = paramiko.SSHClient()
		self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			self._ssh_client.connect(hostname=self.vm_ip, port=self.ssh_port, username='root', password='123456')
			for command in self.commands_dict.iterkeys():
				stdin, stdout, stderr = self._ssh_client.exec_command(command)
				self.ssh_result[command] = {}
				self.ssh_result[command]['stdout'] = stdout.read()
				self.ssh_result[command]['stderr'] = stderr.read()
		finally:
			self._ssh_client.close()
	
	def check_result(self):
		
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
