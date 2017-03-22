import sys

storefront = sys.argv[1].lower()
if storefront == 'old_glory':
    storefront_id = 1
elif storefront == 'animalworld':
    storefront_id = 2

from ebay_api import EbayAPI
from iMerchandise.connection import iMerchConnection
from iMerchandise.tracking import get_shipment_info_for_channel

api = EbayAPI(storefront)

conn = iMerchConnection()

results = conn.get_shipped_orders_not_sent('ebay', storefront)
if not results:
    print 'no orders ready yet'
    sys.exit(0)

external_ids = set([row['external_id'] for row in results])

for external_id in external_ids:

    conn.cursor.execute("SELECT ebay_item_id, ebaytransactionid, sku FROM sales_order_table WHERE external_id = %s;", (external_id,))
    ebay_ids = conn.cursor.fetchall()

    trackinginfo = conn.get_tracking_info(external_id, 'ebay', storefront)

    trackingcode = trackinginfo['trackingcode']
    carrier = trackinginfo['carrier']
    shipment_method = trackinginfo['shipment_method']

    shipment_info = get_shipment_info_for_channel(carrier, shipment_method, 'ebay')
    carrier = shipment_info['carrier']
    shipment_method = shipment_info['shipment_method']


    if trackingcode.startswith("1Z") or trackingcode.startswith('1z'):
        carrier = 'UPS'
    elif trackingcode.startswith('920'):
        carrier = 'USPS'
    elif trackingcode.startswith('927'):
        carrier = "UPS-MI"
    elif trackingcode == '' or trackingcode is None:
        print 'error'
    else:
        carrier = carrier

    if carrier == '':
        print 'error'

    for ebay_id in ebay_ids:
        ebay_item_id = ebay_id['ebay_item_id']
        ebaytransactionid = ebay_id['ebaytransactionid']
        sku = ebay_id['sku']

        print trackingcode, carrier, ebaytransactionid, ebay_item_id

        r = api.complete_sale(trackingcode, carrier, ebaytransactionid, ebay_item_id)
        if r.dict()['Ack'] == 'Success':
            line_item = {
                'external_id': external_id,
                'sales_channel_id': 3,
                # 'ordersku': sku,
                'storefront_id': storefront_id,
            }
            # conn.set_tracking_to_shipped(line_item)
            conn.cursor.execute("UPDATE tracking_table SET trackingset = 'Y', tracking_confirmed = 'Y', tracking_confirmed_modified = NOW() WHERE external_id = %(external_id)s AND sales_channel_id = %(sales_channel_id)s AND storefront_id = %(storefront_id)s;",
                                line_item)
        else:
            sys.stderr.write("Tracking error with %s\n" % external_id)
conn.cursor.execute("UPDATE feedersettings.tracking_last_updated SET last_updated = NOW() WHERE sales_channel_id = 3 AND storefront_id = %s;", (storefront_id,))
