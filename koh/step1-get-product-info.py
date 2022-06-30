"""step1 download all products by categories for sellers

this script only handles downloads of seller item list by category.
this script will retry failed/blocked download until success.
this script can be relaunch and resume from where it left of.
downloaded pages are saved in "shop_category" directory
and later extracted & transformed by step2-script (manual run)


current download issue
- retry blocked link is disabled (to add retry later) as other links may still work
- downloading new link (newly added to seller/category list) will trigger blocker faster (around 3/4 download, need more testing)
- redownload deleted json will trigger blocker much slower (maybe around 10?)
- blocker cooldown around 10minutes (need more testing)
"""

import requests
import os
import csv
import time
import json
import ft

SELLERS = ["senheng", "luster-mobile", 'itworld', 'jws-mobile-shop', 'sentriqmy', 'oneclick-tech-gadget', 
		'littlestore1631861799', 'g-store1629966790', 'lotuss-official-store', 'wow-phone', 'thundermatch', 'directd']
		#  "senq", 
CATEGORIES = ['mobiles', 'tablets', 'laptops','desktop-computer']
BASE_URL='https://www.lazada.com.my/shop-{category}/?ajax=true&from=wangpu&page={page}&{seller}'
# BASE_URL='https://www.lazada.com.my/shop-{category}/?{seller}&ajax=true&from=wangpu&page={page}'
# BASE_URL='https://www.lazada.com.my/shop-{category}/?{seller}&page={page}&from=wangpu&ajax=true'

def main():
	if not os.path.exists(ft.shop_category):
		os.mkdir(ft.shop_category)
	for seller in SELLERS:
		for category in CATEGORIES:
			pg = last_page = 1
			retry = 0
			while pg <= last_page:
				filename = os.path.join(ft.shop_category, "{seller}-{category}-{page}.json".format(category=category, page=pg, seller=seller))
				if os.path.exists(filename):
					f = open(filename)
					data = json.load(f)
					total_results = int(data['mainInfo']['totalResults'])
					page_size = int(data['mainInfo']['pageSize'])
					last_page = int((total_results + page_size - 1) / page_size)
					pg += 1
					continue
				# s = requests.session()
				url = BASE_URL.format(category=category, page=pg, seller=seller)
				res = requests.get(url , headers= {'User-Agent': ft.user_agent()})
				if 'application/json' not in res.headers['content-type']:
					## done retry
					print('fail', url)
					break
					retry = retry + 1
					print('not json, retry after 10sec x', retry)
					time.sleep(retry * 10)
					continue
				retry = 0
				open(filename, 'w', encoding='utf-8').write(res.text)
				data = res.json()
				item_count = len(data['mods']['listItems']) if 'listItems' in data['mods'] else 0
				total_results = int(data['mainInfo']['totalResults'])
				page_size = int(data['mainInfo']['pageSize'])
				last_page = int((total_results + page_size - 1) / page_size)
				print(url)
				# print(seller, category, item_count, total_results, pg, last_page)
				# if (item_count > 0):
				# 	with open(CSV_FILE, 'a', encoding='utf-8') as csvfile:
				# 		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				# 		for item in data['mods']['listItems']:
				# 			spamwriter.writerow([seller, item['name'], item['price'], item['itemUrl']])
				pg += 1
				time.sleep(1)


if __name__ == "__main__":
	main()
