# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import json
import string
import copy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from stemming.porter2 import stem
import operator
import re

#workflow: find a gloss list of all the unesco sites in the world, input that as a search term
# get the href of the first result 
#hit the href of the first result, then parse all the reviews on the first page,
#ping the next page after 'Reviews' insert '-or10' and at the end insert '/BackUrl#REVIEWS' and keep going for every int replacing the 1: ie the 47th page would be 470
#ex:
	#page 1:https://www.tripadvisor.com/Attraction_Review-g608496-d1822321-Reviews-Jatiluwih_Green_Land-Tabanan_Bali.html
	#page 2:https://www.tripadvisor.com/Attraction_Review-g608496-d1822321-Reviews-or10-Jatiluwih_Green_Land-Tabanan_Bali.html/BackUrl#REVIEWS

def find_numpages(url):
	driver = webdriver.PhantomJS()
	driver.get(url)
	time.sleep(2)
	try:		
		pagenums = driver.find_element_by_class_name('pageNumbers').find_elements_by_tag_name("a")
		for pg in pagenums:
			pagestr = pg.text

	except NoSuchElementException:
		print('halp')
	driver.close()
	parse_page(url)
	for page in xrange(1, int(pagestr)):
		nexturl = next_page(url, page)
		print(nexturl)
		parse_page(nexturl)


def parse_page(url):
	#div class="member_info" --> div class="location" contains the text of the City, Country
	#want stars but they are harder to access raw - best way is prob to map image urls to star ratings
	driver = webdriver.PhantomJS()
	driver.get(url)
	time.sleep(2)

		#get links ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		member_infos = driver.find_element_by_id("REVIEWS").find_elements_by_class_name("member_info")
			#this is one level down of where member_infos is
		text_revs = driver.find_element_by_id("REVIEWS").find_elements_by_class_name("partial_entry")
			#this might not really be allowed
		#star_revs = driver.find_element_by_id("REVIEWS").find_elements_by_class_name("innerBubble").find_element_by_tag_name("img")
		

		for member, rtext in zip(member_infos, text_revs):
			print(member.text)
			print(rtext.text)
			print('\n\n')
	except NoSuchElementException:
		print('halp')
			# 	li = ref.get_attribute('href')
	driver.close()


def next_page(url, pagenum):
	newurl = url.replace("Reviews", "Reviews-or-" + str(pagenum) + "0-")
	return newurl + "/BackUrl#REVIEWS"

def search_site(site):
	url = "https://www.tripadvisor.com/Search?geo&redirect&q=" 
	sitewds = re.findall(r"[\w']+", site)
	for w in sitewds:
		url = url + '+' + w
	driver = webdriver.PhantomJS()
	driver.get(url)
	time.sleep(3)
	href_snippet = driver.find_element_by_id("search_result").find_element_by_class_name("title").get_attribute('onclick')
	hrefchars = list(href_snippet)
	record = False
	realhref = 'https://www.tripadvisor.com'
	for c in hrefchars:
		if c == '/':
			record = True
		if record:
			realhref = realhref + str(c)
	print('\n\n')
	realhref = realhref[0:len(realhref)-2]
	return realhref
	
	#ping
	#get href of first result
	#call find_numpages, parse_page and then parse next page parse on that
	
#"https://www.tripadvisor.com/Search?geo&redirect&q=Minaret+and+Archaeological+Remains+of+Jam&uiOrigin=MASTHEAD&ssrc=A&typeaheadRedirect=true&returnTo=__2F__&pid=3825&startTime=1475511818675&searchSessionId=4FD213D3A5F74E7CDE9F09A7026D18651475511721479ssid"
#"https://www.tripadvisor.com/Search?geo=659499&redirect&q=Minaret+and+Archaeological+Remains+of+Jam&uiOrigin&ssrc=A&typeaheadRedirect=true&returnTo=__2F__&pid=3826&startTime&searchSessionId=4FD213D3A5F74E7CDE9F09A7026D18651475511821708ssid"

def parse_text(file):
	#
	pass

def main():
	siteurl = search_site("Pyramids of Giza")
	pagenum = find_numpages(siteurl)

	# parse_page('https://www.tripadvisor.com/Attraction_Review-g608496-d1822321-Reviews-Jatiluwih_Green_Land-Tabanan_Bali.html')
	
if __name__ == '__main__':
	main()

