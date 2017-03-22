import sys
import gzip
import ebay_api

fname = sys.argv[1]
f = open(fname)
xml = f.read()
f.close()
storefront = sys.argv[2]
upload_job_type = sys.argv[3]  # e.g. ReviseFixedPriceItem
assert storefront in ('old_glory', 'animalworld')
api = ebay_api.EbayAPI(storefront)

with gzip.open('inventory.xml.gz', 'w') as f:
    f.write(xml)

response = api.create_upload_job_for_revise_fixed_price_item(upload_job_type)
file_reference_id, job_id = response['file_reference_id'], response['job_id']
print file_reference_id, job_id

api.upload_file_request(job_id, file_reference_id, 'inventory.xml.gz')
api.start_upload_job(job_id)
