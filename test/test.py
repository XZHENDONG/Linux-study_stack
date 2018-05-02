# coding=utf-8
import virtualbox

vbox = virtualbox.VirtualBox()

vm = vbox.find_machine('redhat-stack')
with vm.create_session() as session:
	with session.console.guest.create_session('root', '123456')as gs:
		print '###################'
		print  gs.execute('/bin/ls', ['-al', '/'])
