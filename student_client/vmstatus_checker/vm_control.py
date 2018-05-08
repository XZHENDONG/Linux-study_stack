# -*- coding:utf-8 -*-
import os
import time

import virtualbox
from virtualbox import library

IMAGE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\study_stack.ova'


class StackVM(object):
	def __init__(self, vm_name='study_stack'):
		self.vm_name = vm_name
		self.vbox = virtualbox.VirtualBox()
		self.vm_instance = self.vbox.find_machine(self.vm_name)
	
	def vm_start(self):
		
		self.vm_instance.launch_vm_process(None, 'gui', '')
		
		print 'waiting vm start ...'
		while True:
			
			with self.vm_instance.create_session() as session:
				try:
					with session.console.guest.create_session('root', '123456')as gs:
						gs.execute('/bin/ls', ['/home'], flags=[library.ProcessCreateFlag.wait_for_process_start_only])
						break
				except:
					continue
		print 'done'
	
	def get_ip(self):
		
		if len(self.vm_instance.enumerate_guest_properties('/VirtualBox/GuestInfo/Net/0/V4/IP')[1]) < 1:
			time.sleep(0.2)
		try:
			self.vmip = self.vm_instance.enumerate_guest_properties('/VirtualBox/GuestInfo/Net/0/V4/IP')[1][0]
			return self.vmip
		except IndexError as e:
			return ''
	
	def vm_shutdown(self):
		with self.vm_instance.create_session() as session:
			session.console.power_down()
	
	def vm_export(self):
		appliance = self.vbox.create_appliance()
		self.vm_instance.export_to(appliance, self.vm_name)
		image_export_process = appliance.write('ovf-2.0',
		                                       [library.ExportOptions.create_manifest],
		                                       IMAGE_PATH)
		return image_export_process
	
	def vm_import(self, ova_path=IMAGE_PATH):
		try:
			appliance = self.vbox.create_appliance()
			appliance.read(IMAGE_PATH)
			image_import_process = appliance.import_machines([library.ImportOptions.import_to_vdi])
			return image_import_process
		except IOError as e:
			raise e + ' please make sure the imagefile("' + ova_path + '") is exist;'


if __name__ == '__main__':
	vm_ctl = StackVM()
	vm_ctl.vm_start()
	print vm_ctl.get_ip()
	vm_ctl.vm_shutdown()
