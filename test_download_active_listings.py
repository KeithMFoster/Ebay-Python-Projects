import json
import sys
import time
from requests.exceptions import ConnectionError
from ebay_api.ebay_api import EbayAPI


api = EbayAPI('old_glory')


try:
    page_number = int(sys.argv[1])
except:
    page_number = 1

while True:
    print 'on page {}'.format(page_number)

    fname = "active_inventory/active_ebay_inventory_{}.json".format(page_number)
    try:
        results = api.get_my_ebay_selling(page_number)
    except ConnectionError:
        time.sleep(10)
        results = api.get_my_ebay_selling(page_number)

    data = results.dict()
    total_number_of_pages = int(data['ActiveList']['PaginationResult']['TotalNumberOfPages'])
    pretty_json = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    with open(fname, 'w') as f:
        f.write(pretty_json)

    page_number += 1
    if page_number > total_number_of_pages:
        break
