import scrap

#============================================#
#========= product with variant =============#
#============================================#

def has_variant(page, data, variants, ids, id_vids, i):
    url = scrap.get_url(page)
    name = get_name(page, i)
    variant = variants[i]["name"]
    variant_id = ids[i]
    vid = variants[i]["vid"]
    price = scrap.get_variant_price(data, id_vids, vid)
    stock = scrap.get_variant_stock(data, variant_id)
    category = scrap.get_category(data)
    product = {"productURL": url, "productName": name, "productVariant": variant, "price": price, "stock": stock, "category": category} 
    return (product)


#============================================#
#======= product without variant ============#
#============================================#

def no_variant(page, data):
    url = scrap.get_url(page)
    name = scrap.get_name(page)
    variant = "NULL" 
    price = scrap.get_variant_price(data, [], "0")
    stock = scrap.get_variant_stock(data, "0")
    category = scrap.get_category(data)
    product = {"productURL": url, "productName": name, "productVariant": variant, "price": price, "stock": stock, "category": category}
    return (product)


#============================================#
#== output duplicate product name with "" ===#
#============================================#

def get_name(page, index):
    if index == 0:
        name = scrap.get_name(page)
    else:
        name = "\"\""
    return name

if __name__ == "__main__":
    main()
