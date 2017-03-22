import sys
import time
from ebay_api import EbayAPI


storefront = sys.argv[1]
assert storefront in ('old_glory', 'animalworld')


api = EbayAPI(storefront)
job_id = api.create_active_inventory_report()

for i in range(4):
    time.sleep(120)
    file_reference_id = api.get_job_status_request(job_id)

    if file_reference_id:
        break
else:
    print 'unable to get a file reference id'

api.download_file(job_id, file_reference_id)
