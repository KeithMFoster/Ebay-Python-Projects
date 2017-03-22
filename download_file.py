import ebay_api
import sys

job_id = sys.argv[1]
file_reference_id = sys.argv[2]
storefront = sys.argv[3]

api = ebay_api.EbayAPI(storefront)

api.download_file(job_id, file_reference_id)
