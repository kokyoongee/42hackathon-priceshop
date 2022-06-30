import csv
import re
from bs4 import BeautifulSoup
import json

#============================================#
#==== load the links provided into list =====#
#============================================#

def get_link(file):
    links = []
    with open(file, "r") as file:
        for line in file:
            links.append(line)
    return links


#============================================#
#get json data from page and parse into json #
#============================================#

def json_parser(page):
    soup = BeautifulSoup(page.content, "html.parser")
    script = str(soup.find_all("script")[122])
    data = re.search("(?<=moduleData__ = )(.*);", script).group(1)
    data = json.loads(data)
    return (data)


#============================================#
#===== scrap proudctName from page url ======#
#============================================#

def get_name(page):
    name_search = re.search("products\/(.*)-", page.url)
    if name_search.group():
        return name_search.group(1)
    return "NULL"


#============================================#
#===== scrap proudctURL from page url =======#
#============================================#

def get_url(page):
    url_search = page.url
    if url_search:
        return url_search
    return "NULL"


#============================================#
#======= scrap variants from page ===========#
#============================================#

def get_variants(data):
    variants = []
    target = data["data"]["root"]["fields"]["productOption"]["skuBase"]["properties"]
    for item in target:
        if item["pid"] == "100005939":
            variants = item["values"]
    return(variants)


#============================================#
#==== match variant id with  variant vid ====#
#============================================#

def match_id_vid(data, variants):
    match = []
    paths = data["data"]["root"]["fields"]["productOption"]["skuBase"]["skus"]
    size = len(paths)
    for variant in variants:
        for i in range(size):
            vid = re.search("(?<=:).*(?<=:)(.*)", paths[i]["propPath"]).group(1)
            if vid == variant["vid"]:
                id_vid = {"id": paths[i]["skuId"], "vid": vid}
                match.append(id_vid)
    return match


#============================================#
#=========== scrap variant id ===============#
#============================================#

def get_variant_id(data, nos):
    ids = []
    for i in range(nos):
        id = data["data"]["root"]["fields"]["productOption"]["skuBase"]["skus"][i]["skuId"]
        ids.append(id)
    return ids


#============================================#
#============ scrap variant price ===========#
#============================================#

def get_variant_price(data, id_vids, vid):
    id = "0"
    size = len(id_vids)
    for i in range(size):
        if id_vids[i]["vid"] == vid:
            id = id_vids[i]["id"]
    price = data["data"]["root"]["fields"]["skuInfos"][id]["price"]["salePrice"]["text"]
    return price


#============================================#
#============ scrap variant stock ===========#
#============================================#

def get_variant_stock(data, id):
    stock = data["data"]["root"]["fields"]["skuInfos"][id]["stock"]
    return stock


#============================================#
#============ scrap product stock ===========#
#============================================#

def get_category(data):
    category = data["data"]["root"]["fields"]["skuInfos"]["0"]["dataLayer"]["pdt_category"][1]
    return category


#============================================#
#===== save the scrapped data into csv ======#
#============================================#

def save_csv(list):
    with open("lazada.csv", "w") as file:
        fieldnames = ["productURL", "productName", "productVariant", "price", "stock", "category"]

        csv.writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv.writer.writeheader()
        for item in list:
            csv.writer.writerow(item)
