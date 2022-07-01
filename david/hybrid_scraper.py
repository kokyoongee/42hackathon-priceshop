import os
import pdb
import time
import agents
import config
import utils

def main():
	if os.path.exists(config.CSV_FILE):
		os.remove(config.CSV_FILE)
	for seller in config.SELLERS:
		links = []
		for category in config.CATEGORIES:
			num = 1
			retry = 0
			while True:
				url = config.BASE_URL.format(category=category, page=num, seller=seller)
				res = utils.send_get_request(url, agents=agents.USER_AGENTS)
				if 'application/json' not in res.headers['content-type']:
					print("initial blocker")
					retry += 1
					print('not json, retry after 10sec x', retry)
					time.sleep(retry * 10)
					continue
				data = res.json()
				print("initial success")
				if 'listItems' not in data['mods']:
					break
				for item in data['mods']['listItems']:
					links.append("http:" + item['itemUrl'])
				num += 1
				total_results = int(data['mainInfo']['totalResults'])
				page_size = int(data['mainInfo']['pageSize'])
				max_page = 1 + int((total_results + page_size - 1)/page_size)
				if num >= max_page:
					break
			products = []
			for link in links:
				fail_counter2 = 0
				res = utils.send_get_request(link, agents=agents.USER_AGENTS)
				html_data = utils.extract_html_product_data(res)
				try:
					product = {
						"seller": html_data['seller_elem'].text.strip().lower().replace(" ", "-"),
						"name": html_data['product_name_elem'].text,
						"product_url": res.url,
					}
					product_variants = utils.extract_json_data(res)
					for product_variant in product_variants:
						product['variant'] = product_variant['variant_name']
						product['stock'] = product_variant['stock']
						product['price'] = product_variant['price']
						products.append(product)
						print("Appending success")
				except:
					print("Individual blocker")
					time.sleep(10)
					fail_counter2 += 1
					if fail_counter2 == 3:
						fail_counter2 = 0
						break
					continue
			print("Saving to csv..")
			utils.save_dict_csv(products, config.CSV_FILE)

if __name__ == "__main__":
	main()
