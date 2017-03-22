import sys
import os
import json
import csv

json_dir = sys.argv[1]

rows = []
for page_number, fname in enumerate(sorted(os.listdir(json_dir))):
    data = json.load(open(os.path.join(json_dir, fname)))
    item_array = data['ActiveList']['ItemArray']['Item']

    for item in item_array:
        item_id = item['ItemID']
        parent_sku = item.get('SKU', '')
        quantity = item.get('Quantity', 0)
        variations = item.get('Variations')
        name = ''
        value = ''
        if variations:
            for item_variation in variations['Variation']:
                if type(item_variation) != dict:
                    continue
                sku = item_variation.get('SKU', '')
                quantity = item_variation.get('Quantity', 0)
                variation_specifics_list = item_variation['VariationSpecifics']['NameValueList']

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
                ])

        else:
            sku = parent_sku

            rows.append([
                item_id,
                parent_sku,
                sku,
                quantity,
                name,
                value
            ])

with open('active_ebay_inventory.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['item_id', 'parent_sku', 'sku', 'quantity', 'name', 'value'])
    writer.writerows(rows)
