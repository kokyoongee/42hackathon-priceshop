"""step2 extract & transform pages downloaded by step1

downloaded pages by step1 are in pure json format
each page contains list of products with max 40 item names, prices, instocks
and item links which we will download later for variant & stock balance

this script always start with creating/replacing lazada.csv,
then read all json files in "shop_category" directory,
and append all items seller,item-name,price,link into lazada.csv

the output lazada.csv will be input for step3 for variant details and splitting
example if a product in lazada.csv has 3 variants with different pricing,
it should be split into 3 separate product with individual spec and price.
for products without variant, information could be sufficient to match against priceshop item list
"""

import json
import os
import glob
import csv
import ft

if os.path.exists("lazada.csv"):
	os.remove("lazada.csv")

def tocsv(filename):
	f = open(filename)
	data = json.load(f)
	seller = data['mainInfo']['allProductURL'].replace('/','')
	print(seller, data['mainInfo']['page'], data['mainInfo']['totalResults'])
	if 'listItems' in data['mods']:
		with open('lazada.csv', 'a', encoding='utf-8') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for item in data['mods']['listItems']:
				spamwriter.writerow([seller, item['name'], item['price'], item['itemUrl']])
		f.close()

for file in sorted(glob.glob(os.path.join(ft.shop_category, '*.json'))):
	tocsv(file)
