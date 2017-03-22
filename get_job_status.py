import ebay_api
import sys

job_id = sys.argv[1]
storefront = sys.argv[2]

api = ebay_api.EbayAPI(storefront)

api.get_job_status_request(job_id)
