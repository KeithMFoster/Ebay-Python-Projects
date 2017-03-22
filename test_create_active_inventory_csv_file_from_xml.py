import sys
import csv
from lxml import objectify

fname = sys.argv[1]
storefront = sys.argv[2]
assert storefront in ('old_glory', 'animalworld')
o = objectify.parse(open(fname))
root = o.getroot()

rows = []
for item in root.ActiveInventoryReport.SKUDetails:
    item_id = item.ItemID
    parent_sku = getattr(item, 'SKU', '')
    quantity = getattr(item, 'Quantity')
    variations = getattr(item, 'Variations', '')

    name = ''
    value = ''
    if len(variations):
        for item_variation in variations.Variation:
            sku = getattr(item_variation, 'SKU', '')
            quantity = getattr(item_variation, 'Quantity')
            variation_specifics_list = item_variation.VariationSpecifics.NameValueList

            if type(variation_specifics_list) == list:
                # TODO
                # this is just a work around for now
                # since we do color variations this will
                # have to be fixed

                variation_specifics_list = variation_specifics_list[0]

            name = variation_specifics_list['Name']
            value = variation_specifics_list['Value']
            rows.append([
                item_id,
                parent_sku,
                sku,
                quantity,
                name,
                value,
                storefront,
            ])

    else:
        sku = parent_sku

        rows.append([
            item_id,
            parent_sku,
            sku,
            quantity,
            name,
            value,
            storefront
        ])

with open(storefront + '_active_ebay_inventory.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['item_id', 'parent_sku', 'sku', 'quantity', 'name', 'value', 'storefront'])
    writer.writerows(rows)
