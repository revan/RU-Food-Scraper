#!/bin/python2
from bs4 import BeautifulSoup
import re
import urllib2
import json
import sys

URL_PREFIX = "http://menuportal.dining.rutgers.edu/foodpro/"
outfile = sys.argv[1]

def scrapeNutritionReport(url):
	"""Scrapes a Nutrition Report page, returns name, serving, calories, ingredients"""
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)
	ret = {}

	# Get item name
	try:
		ret['name'] = soup.find(id="content-text").find_all("h2")[1].string
	except AttributeError:
		pass

	# Get serving size
	try:
		ret['serving'] = soup.find(id="facts").find("p", "").string[len("Serving Size "):]
	except AttributeError:
		pass

	# Get calorie count.
	try:
		ret['calories'] = int(soup.find(id="facts").find("p", "strong").string[len("Calories "):])
	except AttributeError:
		pass

	# Get ingredient list
	try:
		e = soup.find(text=re.compile("INGREDIENTS")).parent
		p = e.parent
		e.decompose()
		ret['ingredients'] = p.string
	except AttributeError:
		pass

	return ret

def scrapeMeal(url):
	"""Parses meal, calls for scraping of each nutrition facts"""
	ret = []
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)
	soup.prettify()
	for link in soup.find("div", "menuBox").find_all("a", href=True):
		ret.append(scrapeNutritionReport(URL_PREFIX+link['href']))
	return ret

def scrapeCampus(url):
	"""Calls for the scraping of the meals of a campus"""
	ret = {}
	ret['Breakfast'] = scrapeMeal(url+"&mealName=Breakfast")
	ret['Lunch'] = scrapeMeal(url+"&mealName=Lunch")
	ret['Dinner'] = scrapeMeal(url+"&mealName=Dinner")
	#ret['']=scrapeMeal(url+"&mealName=") #takeout
	return ret

def scrape():
	"""Calls for the scraping of the menus of each campus"""
	prefix = URL_PREFIX + "pickmenu.asp?locationNum=0"
	ret = {}
	ret['Brower Commons'] = scrapeCampus(prefix + str(1))
	ret['Busch Dining Hall'] = scrapeCampus(prefix + str(4))
	ret['Neilson Dining Hall'] = scrapeCampus(prefix + str(5))
	ret['Livingston Dining Commons'] = scrapeCampus(prefix + str(3))
	#where's number two?
	return ret

output = open(outfile, 'w')
json.dump(scrape(), output, indent=1)
output.close()
