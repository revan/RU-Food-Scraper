#!/bin/python2
from bs4 import BeautifulSoup
import re
import urllib2
import sys

outfile = sys.argv[0]

def scrapeNutritionReport(url):
	"""Scrapes a Nutrition Report page, returns name, serving, calories, ingredients"""
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)
	ret = {}
	try:
		ret['name'] = soup.find(id="content-text").find_all("h2")[1].string #name
	except AttributeError:
		pass
	try:
		ret['serving'] = soup.find(id="facts").find("p", "").string[len("Serving Size "):] #serving size
	except AttributeError:
		pass
	try:
		ret['calories'] = int(soup.find(id="facts").find("p", "strong").string[len("Calories "):]) #calories
	except AttributeError:
		pass

	try:
		e = soup.find(text=re.compile("INGREDIENTS")).parent
		p = e.parent
		e.decompose()
		ret['ingredients'] = p.string #ingredients
	except AttributeError:
		pass

	return ret

def scrapeMeal(url):
	"""Parses meal, calls for scraping of each nutrition facts"""
	ret = []
	prefix="http://menuportal.dining.rutgers.edu/foodpro/"
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)
	soup.prettify()
	for link in soup.find("div", "menuBox").find_all("a", href=True):
		ret.append(scrapeNutritionReport(prefix+link['href']))
	return ret

def scrapeCampus(url):
	"""Calls for the scraping of the meals of a campus"""
	ret = {}
	ret['Breakfast']=scrapeMeal(url+"&mealName=Breakfast")
	ret['Lunch']=scrapeMeal(url+"&mealName=Lunch")
	ret['Dinner']=scrapeMeal(url+"&mealName=Dinner")
	#ret['']=scrapeMeal(url+"&mealName=") #takeout
	return ret

def scrape():
	"""Calls for the scraping of the menus of each campus"""
	prefix = "http://menuportal.dining.rutgers.edu/foodpro/pickmenu.asp?locationNum=0"
	ret = {}
	ret['Brower Commons'] = scrapeCampus(prefix + str(1))
	ret['Busch Dining Hall'] = scrapeCampus(prefix + str(4))
	ret['Neilson Dining Hall'] = scrapeCampus(prefix + str(5))
	ret['Livingston Dining Commons'] = scrapeCampus(prefix + str(3))
	#where's number two?
	return ret

output = open(outfile, 'w')
output.write(str(scrape()))
output.close()