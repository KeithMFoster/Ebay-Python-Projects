import datetime
import sys
from ebaysdk.exception import ConnectionError


sys.path.insert(0, '..')
from ebay_api import EbayAPI
from iMerchandise.connection import iMerchConnection

storefront = sys.argv[1]


conn = iMerchConnection()
api = EbayAPI(storefront)

if storefront == 'animalworld':
    storefront_id = 2
elif storefront == 'old_glory':
    storefront_id = 1
else:
    print 'incorrect storefront'
    sys.exit(1)

# last_update_date_file_name = 'last_update_date.txt'
# with open(last_update_date_file_name, 'r') as f:
#     last_update_date = f.read()

# query = """select ps.sku, pi.quantity as `actual_quantity`, ps.name, ps.value, ps.ebay_parent_child, ps.item_id, p.producttype,
# if(p.productstatus = 'R1',
#     if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(r1_enabled = 1, r1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = %(storefront_id)s), 0, if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity)) ,
#     if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(c1_enabled = 1, c1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = %(storefront_id)s), 0, if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity))) as quantity,
# pi.InventoryUpdate
# from redrocket.ebay_inventory as ps
# inner join redrocket.product_inventory as pi on ps.sku = pi.sku
# inner join redrocket.product as p on ps.sku = p.sku
# where ps.on_ebay > 0
# and ps.storefront_id = %(storefront_id)s
# and ps.ebay_parent_child <> 'parent'
# and pi.inventoryupdate > %(last_update_date)s
# """

query = """select ps.sku, pi.quantity as `actual_quantity`, ps.name, ps.value, ps.ebay_parent_child, ps.item_id, p.producttype, pi.virtual_stock_allowed,
if(p.productstatus = 'R1',
    if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(r1_enabled = 1, r1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = %(storefront_id)s), 0, if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity)) ,
    if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(c1_enabled = 1, c1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = %(storefront_id)s), 0, if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity))) as quantity,
pi.InventoryUpdate
from redrocket.ebay_inventory as ps
inner join redrocket.product_inventory as pi on ps.sku = pi.sku
inner join redrocket.product as p on ps.sku = p.sku
inner join redrocket.product_stores as product_stores on product_stores.sku = ps.sku
where ps.on_ebay > 0
and ps.pt_quantity <> pi.quantity
and ps.ebay_parent_child <> 'parent'
and product_stores.storefront_id = %(storefront_id)s
and pi.virtual_stock_allowed = 'N'
"""
# conn.cursor.execute(query, {'storefront_id': storefront_id, 'last_update_date': last_update_date})
conn.cursor.execute(query, {'storefront_id': storefront_id})
# error code 21916750 means already ended

results = conn.cursor.fetchall()

print 'updating %d products...' % (len(results),)
for row in results:
    sku = row['sku']
    item_id = row['item_id']
    name = row['name']
    value = row['value']
    quantity = row['quantity']  # real product quantity
    actual_quantity = row['actual_quantity']
    ebay_parent_child = row['ebay_parent_child']

    producttype = row['producttype']
    print producttype
    print row['actual_quantity'], row['quantity']

    if producttype == 'FINISHED_GOOD':
        if quantity > 10:
            quantity = 10
    else:
        if quantity > 5:
            quantity = 5


    # TODO consolidate the child and lone branch
    if ebay_parent_child == 'child':  # variant of an item on ebay
        try:
            print 'updating %s... to %d inventory' % (sku, quantity)
            api_results = api.update_item_variation(item_id, quantity, name, value)
            print 'successfully updated %s on ebay...' % (sku,)

        except ConnectionError, e:

            errors = e.response.dict()['Errors']
            if type(errors) is list:
                error_codes = [error['ErrorCode'] for error in errors]
            else:
                error_codes = [errors['ErrorCode']]

            if '942' in error_codes:  # At least one of the variations associated with this listing must have a quantity greater than 0
                try:
                    print 'One variation must have a quantity greater than zero. attempting to end.'
                    print 'attempting to end item...'
                    api_results = api.end_item(item_id)
                    print 'ended item...'

                except ConnectionError, e:
                    errors = e.response.dict()['Errors']
                    if type(errors) is list:
                        error_codes = [error['ErrorCode'] for error in errors]
                    else:
                        error_codes = [errors['ErrorCode']]

                    if '1047' in error_codes:  # auction already has been closed
                        print 'auction has been closed already'
                    else:
                        print 'failed to end item'
                        # raise

            elif '291' in error_codes:
                print 'not allowed to revise ended item. ignoring this'

            else:
                print e.response.dict()['Errors']
                print e.response.dict()
                print 'we probably reached the limit of products we can list'
                # raise

        conn.cursor.execute("UPDATE ebay_inventory SET pt_quantity=%s WHERE sku=%s;", (actual_quantity, sku))
        print 'updated database...'

    else:  # ebay lone with no variants
        try:
            print 'updating %s...' % (sku,)
            api_results = api.update_inventory(item_id, quantity)
            print 'successfully updated %s on ebay...' % (sku,)

        except ConnectionError, e:

            errors = e.response.dict()['Errors']
            if type(errors) is list:
                error_codes = [error['ErrorCode'] for error in errors]
            else:
                error_codes = [errors['ErrorCode']]

            if '515' in error_codes:  # The quantity must be a valid number greater than 0.
                try:
                    print 'attempting to end item...'
                    api_results = api.end_item(item_id)
                    print 'ended item...'

                except ConnectionError, e:
                    errors = e.response.dict()['Errors']
                    if type(errors) is list:
                        error_codes = [error['ErrorCode'] for error in errors]
                    else:
                        error_codes = [errors['ErrorCode']]

                    if '1047' in error_codes: # auction already has been closed
                        print 'auction has been closed already'
                    else:
                        print 'failed to close auction'
                    #     raise

            elif '21916750' in error_codes: # not allowed to revise ended item
                # can ignore this for now
                print 'not allowed to revise ended item. ignoring this'
            else:
                print e.response.dict()['Errors']
                print 'we probably reached the limit of products we can list'
                # raise

        conn.cursor.execute("UPDATE ebay_inventory SET pt_quantity=%s WHERE sku=%s;", (actual_quantity, sku))
        print 'updated database...'

# last_update_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# with open(last_update_date_file_name, 'w') as f:
#     f.write(last_update_date)
