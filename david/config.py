import datetime

SELLERS = [
	# "senheng",
	# "jws-mobile-shop",
	"luster-mobile",
	# "senq"
	]
CATEGORIES = [
	# 'processors',
	# 'mobiles',
	# 'laptops',
	'tablets',
	# 'processors',
	# 'graphic-cards',
	# 'motherboards'
	]

BASE_URL = 'https://www.lazada.com.my/shop-{category}/?ajax=true&from=wangpu&page={page}&{seller}'

CSV_FILE = 'lazada{date}.csv'.format(date=datetime.date.today().strftime("%d%m%Y"))
