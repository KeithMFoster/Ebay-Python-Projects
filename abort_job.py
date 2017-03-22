import ebay_api
import sys

storefront = sys.argv[1]
job_id = sys.argv[2]

print job_id
api = ebay_api.EbayAPI(storefront)

api.abort_job(job_id)