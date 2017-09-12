# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import os


def rename_wf802(device_type):
	'''
	wave2.CIG.R3.1.00.B028.nand2
	if file name type change ,we should change files[10:]
	:return:
	'''
	os.chdir('/home/share/robot_test/WF802s_AutoUpgrade/version/%s/new/'%device_type)
	path = '/home/share/robot_test/WF802s_AutoUpgrade/version/%s/new/'%device_type
	files = os.listdir(path)
	for file in files:
		os.system('rm -rf *')
	os.chdir('/home/share/robot_test/WF802s_AutoUpgrade/version/%s/old/'%device_type)
	os.system('cp *.* /home/share/robot_test/WF802s_AutoUpgrade/version/%s/new/'%device_type)
	os.chdir('/home/share/robot_test/WF802s_AutoUpgrade/version/%s/new/'%device_type)
	PATH = '/home/share/robot_test/WF802s_AutoUpgrade/version/%s/new/'%device_type
	filelist = os.listdir(PATH)
	for files in filelist:
		new_file = files[10:]
		old_dir = os.path.join(PATH, files)
		new_dir = os.path.join(PATH, new_file)
		os.renames(old_dir, new_dir)




