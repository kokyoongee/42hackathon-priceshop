import json
import time
import csv
import random
import requests
from bs4 import BeautifulSoup
import pdb


def extract_json_data(response_obj):
	json_data = json.loads(response_obj.text.split("__moduleData__ =")[1].split('\n')[0].strip(';'))
	products = [] # final array of product dictionaries
	color_variants = []
	specification_variant = []
	variant_types = json_data['data']['root']['fields']['productOption']['skuBase']['properties']
	skus = json_data['data']['root']['fields']['productOption']['skuBase']['skus']
	for variant_type in variant_types:
		if "Color" in variant_type['name'] or "color" in variant_type['name']:
			for color in variant_type['values']:
				color_variants.append({
					'color_spec_id': variant_type['pid'],
					'color_id': color['vid']
					})
		else:
			for specification in variant_type['values']:
				specification_variant.append({
					'spec_id': variant_type['pid'],
					'variant_name': specification['name'],
					'variant_id': specification['vid'],
				})
	cart_sku_id_groups = []
	if len(specification_variant) > 0:
		for sku in skus:
			variant_name = ""
			same_spec_sku = []
			for specification in specification_variant:
				if '{spec_id}:{variant_id}'.format(spec_id=specification_variant['spec_id'], variant_id=specification_variant['variant_id']) \
					in sku['propPath']:
					variant_name = specification_variant['variant_name']
					same_spec_sku.append(sku['cartSkuId'])
			cart_sku_id_groups.append((variant_name, same_spec_sku))
	else:
		same_spec_sku = []
		for sku in skus:
			for color_variant in color_variants:
				if '{spec_id}:{variant_id}'.format(spec_id=color_variant['color_spec_id'], variant_id=color_variant['color_id']) \
					in sku['propPath']:
					same_spec_sku.append(sku['cartSkuId'])
		cart_sku_id_groups.append(("", same_spec_sku))
	available_cart_sku_ids = json_data['data']['root']['fields']['skuInfos'] # dictionary
	for sku_group in cart_sku_id_groups:
		stock = 0
		price = 0
		for sku_id in sku_group[1]:
			stock += available_cart_sku_ids[sku_id]['stock']
			price = available_cart_sku_ids[sku_id]['price']['salePrice']['value']
		products.append({
			'variant_name': sku_group[0],
			'stock': stock,
			'price': price
		})
	return products

def extract_html_product_data(response_obj):
	page_soup = BeautifulSoup(response_obj.text, 'html.parser')
	return {
		"seller_elem" : page_soup.find("a", {"class": "pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name"}),
		"product_name_elem" : page_soup.find("h1", {"class": "pdp-mod-product-badge-title"}),
		"price_elem" : page_soup.find("div", {"class": "pdp-product-price"})
	}

'''
Save the data input (dictionary) as an array into csv
'''
def save_dict_csv(array, file):
	fieldnames = sorted(array[0].keys()) if array else None
	with open(file, 'a', encoding='UTF-8') as csvfile:
		spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in array:
			spamwriter.writerow(item)

'''
Creates a new session, waits for random delay before sending get request
'''
def send_get_request(url, agents):
	headers = {'user-agent': agents[random.randrange(0, len(agents))]}
	time.sleep(max(random.gauss(3,1),2))
	res = requests.get(url=url, headers=headers)
	return res
