#!/bin/python
from bs4 import BeautifulSoup
from re import compile
try:
	from urllib2 import urlopen
except:
	from urllib.request import urlopen
import json
from sys import stdout
from argparse import ArgumentParser, FileType

parser = ArgumentParser(prog='RU Food Scraper', description='Scrape the Rutgers' +
                        'Dining Website for nutritional information\n' +
                        'Prints output as json.')
parser.add_argument('outfile', nargs='?', type=FileType('w'), default=stdout,
                    help="Output file (defaults to stdout).")
parser.add_argument('--fancy', dest='fancy', action='store_true', default=False)
args = parser.parse_args()

ingredientSplit = compile(r'(?:[^,(]|\([^)]*\))+')
URL_PREFIX = "http://menuportal.dining.rutgers.edu/foodpro/"

def scrapeNutritionReport(url):
	"""Scrapes a Nutrition Report page, returns name, serving, calories, ingredients"""
	page = urlopen(url).read()
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
		e = soup.find(text=compile("INGREDIENTS")).parent
		p = e.parent
		e.decompose()
		ret['ingredients'] = [ing.strip() for ing in ingredientSplit.findall(p.string)]
	except AttributeError:
		pass

	return ret

def scrapeMeal(url):
	"""Parses meal, calls for scraping of each nutrition facts"""
	page = urlopen(url).read()
	soup = BeautifulSoup(page)
	soup.prettify()
	return [scrapeNutritionReport(URL_PREFIX + link['href']) for link in
	        soup.find("div", "menuBox").find_all("a", href=True)]

def scrapeCampus(url):
	"""Calls for the scraping of the meals of a campus"""
	# TODO: Add takeout?
	meals = ('Breakfast', 'Lunch', 'Dinner')
	return {meal: scrapeMeal(url + "&mealName=" + meal) for meal in meals}

def scrape():
	"""Calls for the scraping of the menus of each campus"""
	prefix = URL_PREFIX + "pickmenu.asp?locationNum=0"
	# There doesn't seem to be a hall #2
	halls = (('Brower Commons', '1'), ('Livingston Dining Commons', '3'),
	         ('Busch Dining Hall', '4'), ('Neilson Dining Hall', '5'))
	return {hall[0]: scrapeCampus(prefix + hall[1]) for hall in halls}

if args.fancy:
	json.dump(scrape(), args.outfile, indent=1)
else:
	json.dump(scrape(), args.outfile)
args.outfile.close()
