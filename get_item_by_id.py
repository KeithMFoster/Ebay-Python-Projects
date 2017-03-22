import sys
import pprint
from ebay_api import EbayAPI

api = EbayAPI(sys.argv[1])

r = api.get_item_by_id(sys.argv[2])
pprint.pprint(r.dict())

