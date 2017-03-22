import sys
from ebay_api.helpers import create_ebay_revise_xml_file


storefront = sys.argv[1]
assert storefront in ('animalworld', 'old_glory')


xml = create_ebay_revise_xml_file(storefront)

with open("revise.xml", 'w') as f:
    f.write(xml)
