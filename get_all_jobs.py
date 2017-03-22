import ebay_api
import sys

storefront = sys.argv[1]

api = ebay_api.EbayAPI(storefront)

api.get_all_created_jobs()