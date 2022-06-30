"""step3 download individual product for variant details

this script simply downloads all products from lazada.csv since it doesnt know if there are product variant 
this script uses different user-agent plus 1sec delay to avoid blocker (seems working), otherwise after 100req, blocker last 30min
this script will retry failed/blocked download until success.
this script can be relaunch and resume from where it left of.
downloaded pages are saved in "products" directory and later extracted & transformed by step4-script (manual run)
"""

import requests
import re
import os
import time
import ft

def main():
	links = get_link("lazada.csv")
	if not os.path.exists(ft.products):
		os.mkdir(ft.products)

	idx = 0;
	for link in links:
		# todo filename too long error
		filename = os.path.join(ft.products, re.sub('[^0-9a-zA-Z]+', '-', link))
		errorfile = 'error-' + filename
		retry = 0
		while not os.path.exists(filename):
			res = requests.get(link, headers = {'user-agent': ft.user_agent()})
			idx += 1
			pos = res.text.find("var __moduleData__")
			if pos > -1:
				retry = 0
				print(link)
				open(filename, 'w', encoding='utf-8').write(res.text)
				if os.path.exists(errorfile):
					os.remove(errorfile)
				time.sleep(1)
			else:
				retry = retry + 1
				print(retry, errorfile)
				open(errorfile, 'w', encoding='utf-8').write(res.text)
				time.sleep(retry * 30)

# load the links provided into list
def get_link(file):
	links = []
	with open(file, "r") as file:
		for line in file:
			links.append('https://' + line.split('//', 2)[1].strip())
	return links

# # save the data scrapped into csv
# def save_csv(list):
# 	with open("lazada.csv", "w") as file:
# 		file.write("productName,price\n")
# 		for item in list:
# 			name 
# 			file.write(f"{item['title']},{item['price']}\n")


if __name__ == "__main__":
	main()