#! /usr/bin/env python
# author: Htut Khine Htay Win 
# version: 1.0
# credit: API from www.youtube2mp3.cc 
# disclaimer: I do not endorse infringement of any copyrighted materials. This is a fun project. 
# Feel free to use it as is. 
# contact: htutkhwin@gmail.com
import os
import re
import time
import Tkinter
from tkFileDialog import askdirectory 
from selenium import webdriver
import selenium.webdriver.chrome.service

# sample code for tkinter use popup window for directory
def getdir(default): 
	window = Tkinter.Tk()
	window.withdraw()
	dir = askdirectory(initialdir=default)
	window.destroy() 
	return dir

def formatMp3Link(id): 
	ID = re.search('=[\w\d_-]{11}', id)
	link = "http://www.youtube2mp3.cc/api/#" + ID.group(0)[1:] + "|mp3"
	return link 

def closeDriver(service, driver): 
	driver.quit() 
	service.stop() 

def openService(link):
	service = selenium.webdriver.chrome.service.Service('/Users/sudo/Dropbox/Workspace/Utility/youtubeTomp3/chromedriver')
	service.start()
	return service
	# binary, chrome finder

def openDriver(service): 
	cap = {'chrome.binary': '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'}
	driver = webdriver.Remote(service.service_url, cap)
	return driver

def downloadFile(driver, link): 
	driver.get(link)
	page = driver.page_source
	buttons = driver.find_element_by_xpath("/html/body/div[@id='converter_background']/div[@id='converter']/div[@id='buttons']/a[1]")
	downloadlink = buttons.get_attribute("href")
	title = driver.find_element_by_xpath("/html/body/div[@id='converter_background']/div[@id='converter']/div[@id='title']").text + ".mp3"
	nospacetitle = title.replace(" ","_").replace("[", "").replace("]", "")
	line = 1
	if (findfile(nospacetitle) == False): 
		print "Downloading: ",link, nospacetitle
		driver.get(downloadlink)
		line += 1
	
	while (findfile(nospacetitle) == False):
		time.sleep(10)

def findfile(title): 
	dir = os.listdir("/Users/sudo/Downloads/")
	exists = False
	for files in dir:
		dcode = files.decode("utf-8")
		ecode = dcode.encode("ascii", "ignore")
		if (ecode == title.encode("ascii", "ignore")): 
				exists = True 
	return exists

def main(): 
	os.chdir("/Users/sudo/Dropbox/Workspace/Utility/youtubeTomp3/")
	linksfile = open("download.list")
	for file in  linksfile.readlines():
		videoId = formatMp3Link(file)
		service = openService(videoId)
		driver = openDriver(service)
		downloadFile(driver, videoId)
		closeDriver(service, driver)
	linksfile.close()
	print "Download complete"

if __name__ == "__main__": 
	main() 
