import requests
import json
import re
import scrap
import variant as var

# - load product web links 
# - requests each link
# - find json content from the web html and parse into json
# - scrap the product data required from json
# - save into csv file

def main():
    products = []    
    links = scrap.get_link("lazada_links.txt")
    s = requests.session()

    for link in links:
        page = s.get(link)
        data = scrap.json_parser(page)
        variants = scrap.get_variants(data)
        nos = len(variants)
        if nos:
            ids = scrap.get_variant_id(data, nos)
            id_vids = scrap.match_id_vid(data, variants)
            for i in range(nos):
                product = var.has_variant(page, data, variants, ids, id_vids, i)
                products.append(product)
        else:
            product = var.no_variant(page, data)
            products.append(product)

    scrap.save_csv(products)

if __name__ == "__main__":
    main()
