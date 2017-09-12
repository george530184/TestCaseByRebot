# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import time
from cap import ssdp_discovery
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
CAP_IPADDR = ssdp_discovery()

def hello_world():
	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Firefox()
	driver.get('http://' + CAP_IPADDR + '/upgrade.html')
	driver.switch_to_frame('iframeallfirst')
	print driver.find_elements_by_xpath('//*[@class="tabulator-col-title"]')[1].text

if __name__=="__main__":
	hello_world()
