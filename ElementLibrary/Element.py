# -*- coding: utf-8 -*-
__author__ = 'Jerry'

import time
from cap import ssdp_discovery
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException

CAP_IPADDR = ssdp_discovery()


class Element(object):
	def __init__(self):
		pass

	def cap_is_element_exits(self):
		'''
		Only upgrade CAP by OTA
		:return:None
		'''
		print 'Upgrade CAP Now!'
		display = Display(visible=0, size=(800, 600))
		display.start()
		driver = webdriver.Firefox()
		driver.get('http://' + CAP_IPADDR + '/upgrade.html')
		driver.switch_to_frame('iframeallfirst')
		try:
			img_checkbox_num = len(driver.find_elements_by_xpath(
				'//*[@class = "tabulator-table"]/div/div/img/parent::*/parent::div/div/input[@class="upgradeCheckbox"]'))
			driver.find_elements_by_xpath(
				'//*[@class = "tabulator-table"]/div/div/img/parent::*/parent::div/div/input[@class="upgradeCheckbox"]')[
				img_checkbox_num - 1].click()  # checkbox
			driver.find_element_by_id("selectmod").find_element_by_xpath("//option[@value='otamode']").click()
			driver.find_element_by_id("BtnUpgrade").click()
			time.sleep(1)
			accept = driver.switch_to_alert()
			accept.accept()
			time.sleep(1)
			display.stop()
			driver.quit()

		except NoSuchElementException as e:
			print 'No CAP in the device list'
			print e
			display.stop()
			driver.quit()
			return False

	def re_is_element_exists(self):
		'''
		Only Upgrade RE by OTA
		:return:None
		'''
		print 'Upgrade RE now'
		display = Display(visible=0, size=(800, 600))
		display.start()
		driver = webdriver.Firefox()
		driver.get('http://' + CAP_IPADDR + '/upgrade.html')
		driver.switch_to_frame('iframeallfirst')
		try:
			upgradeable_num = len(driver.find_elements_by_xpath(
				'//*[name()="svg"]/parent::*/parent::div/div/input[@class="upgradeCheckbox"]'))
			for i in range(upgradeable_num):
				driver.find_elements_by_xpath(
					'//*[name()="svg"]/parent::*/parent::div/div/input[@class="upgradeCheckbox"]')[
					i].click()  # all_checkbox
			time.sleep(1)
			img_cap_num = len(driver.find_elements_by_xpath(
				'//*[@class = "tabulator-table"]/div/div/img/parent::*/parent::div/div/input[@class="upgradeCheckbox"]'))
			driver.find_elements_by_xpath(
				'//*[@class = "tabulator-table"]/div/div/img/parent::*/parent::div/div/input[@class="upgradeCheckbox"]')[
				img_cap_num - 1].click()  # cap_checkbox
			driver.find_element_by_id("selectmod").find_element_by_xpath("//option[@value='otamode']").click()
			driver.find_element_by_id("BtnUpgrade").click()
			time.sleep(1)
			accept = driver.switch_to_alert()
			accept.accept()
			time.sleep(1)
			display.stop()
			driver.quit()

		except NoSuchElementException as e:
			print 'RE is the latest version.'
			print e
			display.stop()
			driver.quit()
			return False

	def judge_page_dead(self):
		'''
		不断刷新页面，若页面死掉，则无法判断页面是否包含某个元素内容，如第一行的CAP，表示CAP重启。
		由此来规避组网升级的时间，最长15min。
		需判断升级失败，均不重启，加超时机制。以免程序死循环
		:return:
		'''
		display = Display(visible=0, size=(800, 600))
		display.start()
		driver = webdriver.Firefox()
		driver.get('http://' + CAP_IPADDR + '/upgrade.html')
		flag_count = 0
		while 1:
			driver.refresh()
			time.sleep(10)
			try:
				driver.switch_to_frame('iframeallfirst')

			except NoSuchFrameException as e:
				break

			CAP = driver.find_elements_by_xpath('//*[@class="tabulator-col-title"]')[1].text
			try:
				if CAP:
					flag_count += 1
					if flag_count == 89:  # 90*10=900s
						break

					else:
						print 2
						continue

			except NoSuchElementException as e:
				break

		display.stop()
		driver.quit()

	def jdge_cap_pass_again(self):
		'''
		通过判断再次获取到CAP的IP地址来规避到重启+选举时间
		加超时保护机制,socket 10s timeout
		:return:
		'''
		get_ip_count = 0
		while 1:
			Get_IP = ssdp_discovery()
			if Get_IP != None:
				break
			else:
				get_ip_count += 1
				if get_ip_count == 89:
					break
				else:
					continue
