import sys
import pprint
from ebay_api import EbayAPI

api = EbayAPI(sys.argv[1])

try:
    sku = sys.argv[3]
except IndexError:
    sku = None
r = api.relist_fixed_price_item(sys.argv[2], sku=sku)
pprint.pprint(r.dict())
