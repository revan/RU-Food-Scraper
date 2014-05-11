#Rutgers Nutritional Information Scraper

Scrapes food.rutgers.edu for menus and nutritional information, saves to file.

Official website reports wonky numbers, so only scraping calories, serving size, and ingredients for now.

###Format

```
{
	'Brower Commons' : {
		'Breakfast' : {
			'CATEGORY' : [
				{
					'name' : 'ITEM NAME',
					'serving' : 'SERVING SIZE',
					'calories' : 100,
					'ingredients' : [
						'INGREDIENT1',
						'INGREDIENT2',
						...
					]
				},
				{
					...
				},
				...
			]
		},
		'Lunch' : {
			...
		},
		'Dinner' : {
			...
		}
	},
	'Busch Dining Hall' : {
		...
	},
	'Neilson Dining Hall' : {
		...
	},
	'Livingston Dining Commons' : {
		...
	}
}
```

###Dependencies
Python script requires package `BeautifulSoup`.