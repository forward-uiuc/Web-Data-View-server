#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import call
import sys
import os 
import time 
import re
import urllib2
import urllib
import requests
import json


class test_amazon_title_price:
	def __init__(self):
		self.filename = "title_price_amazon_2.json"
		self.page = "file:///Users/apple/Downloads/QueryLanguageProjectSpring2018/Webdataview-backend-tryremoving/Queries/am.htm" #"https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=laptop"
		self.expected = 30
	def test(self):	
		pb = execute_query(self.filename, self.page)
		self.check_result(pb)
	def check_result(self, pb):
		# Select records field
		pb.switch_to_default_content()
		pb.find_element_by_xpath("//div[@class='a-fixed-left-grid-col a-col-left'][1]").click()
		pb.switch_to_frame(pb.find_element_by_xpath("//iframe[@id='webview-tooltip']"))
		pb.find_element_by_xpath("//i[@id='web-view-expand-selection']").click()
		pb.switch_to_frame(pb.find_element_by_xpath("//iframe[@id='webview-tooltip']"))
		pb.find_element_by_xpath("//i[@id='web-view-expand-selection']").click()
		pb.switch_to_frame(pb.find_element_by_xpath("//iframe[@id='webview-tooltip']"))
		pb.find_element_by_xpath("//i[@id='cap_toggle']").click()
		pb.find_element_by_xpath("//input[@id='filter_class']").click()
		pb.switch_to_default_content()
		pb.switch_to_frame(pb.find_element_by_xpath("//iframe[@id='webdataview-widget-iframe']"))
		pb.find_element_by_xpath("//div[@id='widget-labels']//li[2]").click()
		pb.switch_to_default_content()
		pb.switch_to_frame(pb.find_element_by_xpath("//iframe[@class='content-frame-default-iframe delete_label_class']"))
		pb.find_element_by_xpath("//button[@class='btn btn-success']").click()
		pb.switch_to_default_content()
		pb.switch_to_frame(pb.find_element_by_xpath("//iframe[@id='webdataview-widget-iframe']"))
		pb.find_element_by_xpath("//i[@id='select-apply']").click()
		pb.find_element_by_xpath("//i[@id='grid-view']").click()
		# Check table results
		time.sleep(1)
		pb.switch_to_window(pb.window_handles[1])
		content = pb.page_source
		actual_result = re.findall('tr role="row" class=', content, re.S)
		# Print test result message
		if len(actual_result) == self.expected:
			print "%s -------------------------- Query Passed" % self.filename
		else:
			print "%s -------------------------- Query Failed" % self.filename
		time.sleep(1000)		


def execute_query(filename, page):
	# Read query from file
	query = ""
	try:
		f = open(filename, 'rb')
	except IOError:
		print "Could not read file:", filename
		sys.exit()
	with f:
		query = f.read()

	# Start Chrome with Web-Data-View
	executable_path = "/usr/local/bin/chromedriver"	# Path of chromedriver
	os.environ["webdriver.chrome.driver"] = executable_path
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("load-extension=/Users/apple/Downloads/Web-Data-View/ng-dashboard")	# Path of Web-Data-View to be tested
	pb = webdriver.Chrome(executable_path = executable_path, chrome_options = chrome_options)
	pb.get(page)

	# Enable Web-Data-View by sikuli script
	call(["/Users/apple/Downloads/runsikulix", "-r", "/Users/apple/Downloads/QueryLanguageProjectSpring2018/Webdataview-backend-tryremoving/Queries/startExtension.sikuli"]) # Path of sikulix and sikuli script
	try:
		wait = WebDriverWait(pb, 20).until(EC.presence_of_element_located((By.ID, "webdataview-floating-widget")))
	except Exception:
		print "Web-Data-View is not enabled.\n"
		pb.quit()
		sys.exit()
	
	# Send query to server
	time.sleep(2)
	pb.switch_to_frame(pb.find_element_by_xpath("//iframe[@id='webview-query']"))
	pb.find_element_by_xpath("//input[@id='username']").send_keys(u"ychen380")
	pb.find_element_by_xpath("//input[@id='login']").click()
	pb.find_element_by_xpath("//textarea[@id='messageName']").send_keys(u"q1")
	pb.find_element_by_xpath("//textarea[@id='messageDesc']").send_keys(query)
	pb.find_element_by_xpath("//div[@class='form-group']/input").click()
	visualize = WebDriverWait(pb, 10).until(EC.element_to_be_clickable((By.ID, "visib_button")))
	visualize.click()
	return pb


def main():
	t = test_amazon_title_price()
	t.test()
	



if __name__ == '__main__':
	main()