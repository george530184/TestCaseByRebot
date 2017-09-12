# -*- coding: utf-8 -*-


__author__ = 'Jerry'

import socket
import telnetlib
import re
import time


SSDP_S = 'uuid:ijklmnop-7dec-11d0-a765-00a0c91e6bf6'
SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 1
SSDP_ST = "CIG:CAP"
USERNAME = 'root'
PASSWORD = 'admin'
cap_ssid_pwd = []
timeout = 10
socket.setdefaulttimeout(timeout)

class CAP(object):
	def __init__(self):
		pass

	def ssdp_discovery(self):
		'''
		SSDP Discovery ,TO get IP address of Server
		:return: IPaddress
		'''
		ssdpRequest = ("M-SEARCH * HTTP/1.1\r\n" + \
					   "S: %s\r\n" % (SSDP_S) + \
					   "HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
					   "MAN: \"ssdp:discover\"\r\n" + \
					   "ST: %s\r\n" % (SSDP_ST) + "\r\n" + \
					   "MX: %d\r\n" % (SSDP_MX)).encode(encoding='utf-8')

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(ssdpRequest, (SSDP_ADDR, SSDP_PORT))
		try:
			data, addr = sock.recvfrom(65535)
			return addr[0]
			sock.close

		except socket.timeout as e:
			print e
			sock.close

	def get_pwd(self):
		try:
			tn = telnetlib.Telnet(host=self.ssdp_discovery(), port=23, timeout=10)
			tn.set_debuglevel(2)
			tn.read_until('Login as:'.encode('utf-8'))  # !str
			tn.write(USERNAME.encode('ascii') + b'\n')  # str
			tn.read_until('Password:'.encode('utf-8'))
			tn.write(PASSWORD.encode('ascii') + b'\n')
			tn.read_until('AP>'.encode('utf-8'))
			tn.write('enable \n'.encode('ascii'))
			tn.read_until('#AP>'.encode('utf-8'))
			tn.write("system/shell \n".encode('ascii'))
			tn.read_until('#AP/system/shell>'.encode('utf-8'))
			tn.write("cd tmp \n".encode('ascii'))
			tn.read_until('#AP/system/shell>'.encode('utf-8'))
			tn.write("cat ath00.conf \n".encode('ascii'))
			time.sleep(1)
			ret = tn.read_very_eager()
			ssid = re.findall(r'ssid=(.*)\r\n'.encode('utf-8'), ret)[0].decode('utf-8')
			pwd = re.findall(r'wpa_passphrase=(.*)\r\n'.encode('utf-8'), ret)[0].decode('utf-8')
			cap_ssid_pwd.append(ssid)
			cap_ssid_pwd.append(pwd)
			tn.close()
			return cap_ssid_pwd[1]

		except Exception as e:
			print e

