import gzip
import ebay_api
import sys
from ebay_api.helpers import create_ebay_revise_xml_file


storefront = sys.argv[1]
assert storefront in ('animalworld', 'old_glory')


xml = create_ebay_revise_xml_file(storefront)

fname = storefront + "_revise.xml"

with open(fname, 'w') as f:
    f.write(xml)

upload_job_type = 'ReviseFixedPriceItem'  # e.g. ReviseFixedPriceItem

api = ebay_api.EbayAPI(storefront)

with gzip.open('inventory.xml.gz', 'w') as f:
    f.write(xml)

response = api.create_upload_job_for_revise_fixed_price_item(upload_job_type)
file_reference_id, job_id = response['file_reference_id'], response['job_id']
print file_reference_id, job_id

api.upload_file_request(job_id, file_reference_id, 'inventory.xml.gz')
api.start_upload_job(job_id)