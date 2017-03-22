import sys
sys.path.insert(0, '..')
from ebay_api.ebay_api import EbayAPI
import csv

# api = EbayAPI('old_glory')

f = open(sys.argv[1], 'r')
reader = csv.DictReader(f)
line = next(reader)
action = line['*Action(SiteID=US|Country=US|Currency=USD|Version=403|CC=UTF-8)']
items = []
while True:
    try:
        assert action.lower() == 'add'
    except AssertionError:
        break
    action = line['*Action(SiteID=US|Country=US|Currency=USD|Version=403|CC=UTF-8)']
    category = line['*Category']
    store_category = line['StoreCategory']
    title = line['*Title']
    upc = line['Product:UPC']
    main_url = line['PicURL']
    relationship = line['Relationship']

    condition_id = line['*ConditionID']
    description = line['*Description']
    style = line['C:Style']
    sleeve_length = line['C:Sleeve Length']
    size_type = line['C:Size Type']
    brand = line['C:Brand']
    material = line['C:Material']
    format = line['*Format']
    duration = line['*Duration']
    sku = line['CustomLabel']
    start_price = line['*StartPrice']
    quantity = line['*Quantity']
    location = line['*Location']
    paypal_email = line['*Location']

    relationship_details = line['RelationshipDetails']

    # size_and_colors = []
    # variations = relationship_details.split('|')
    # for variation in variations:
    #     print variation
    #     name, values_s = variation.split('=')
    #     values = values_s.split(';')
    #     size_and_colors.append((name, values))

    item = {
        'Item': {
            'SKU': sku,
            'InventoryTrackingMethod': 'SKU',
            'ConditionID': condition_id,
            'ListingDuration': 'GTC',
            'Currency': 'USD',
            'Country': 'US',
            'PrimaryCategory': {'CategoryID': category},
            'Location': 'US',
            'Title': title,
            'Description': description,
            'PaymentMethods': ['PayPal', 'CreditCard'],
            'PayPalEmailAddress': 'payments@webfillment.com',
            'DispatchTimeMax': '1',
            'ItemSpecifics': {'NameValueList': [
                {'Name': 'Size Type', 'Value': size_type}, {'Name': 'Brand', 'Value': brand}, {'Name': 'Style', 'Value': style}, {'Name': 'Material', 'Value': material}
            ]},
            'PictureDetails': {
                'PictureURL': main_url,
            },
            'ReturnPolicy': {
                'ReturnsAcceptedOption': 'ReturnsAccepted',
                'RefundOption': 'MoneyBack',
                'ReturnWithinOption': 'Days_30',
            },
            'ShippingDetails': {
                'ShippingServiceOptions': [
                    {
                        'ShippingServicePriority': '1',
                        'ShippingService': 'ShippingMethodStandard',
                        'ShippingServiceCost': '5.95',
                        'ShippingServiceAdditionalCost': '1.00',
                    },
                    {
                        'ShippingServicePriority': '2',
                        'ShippingService': 'UPS2ndDay',
                        'ShippingServiceCost': '13.95',
                        'ShippingServiceAdditionalCost': '1.00',
                    },
                    {
                        'ShippingServicePriority': '3',
                        'ShippingService': 'UPSNextDay',
                        'ShippingServiceCost': '25.95',
                        'ShippingServiceAdditionalCost': '1.00',
                    },
                ]
            },
        }
    }
    item['Item']['Variations'] = {}
    item['Item']['Variations']['Pictures'] = []

    line = next(reader)
    variations = []
    while True:
        action = line['*Action(SiteID=US|Country=US|Currency=USD|Version=403|CC=UTF-8)']
        assert action == ''
        category = line['*Category']
        store_category = line['StoreCategory']
        title = line['*Title']
        upc = line['Product:UPC']
        main_url = line['PicURL']
        relationship = line['Relationship']

        condition_id = line['*ConditionID']
        description = line['*Description']
        style = line['C:Style']
        sleeve_length = line['C:Sleeve Length']
        size_type = line['C:Size Type']
        brand = line['C:Brand']
        material = line['C:Material']
        format = line['*Format']
        duration = line['*Duration']
        sku = line['CustomLabel']
        start_price = line['*StartPrice']
        quantity = line['*Quantity']
        location = line['*Location']
        paypal_email = line['*Location']

        relationship_details = line['RelationshipDetails']

        try:
            line = next(reader)
        except StopIteration:
            break

        action = line['*Action(SiteID=US|Country=US|Currency=USD|Version=403|CC=UTF-8)']
        if action.lower() == 'add':
            break
    item['Item']['Variations'] = variations
    items.append(item)

# fixed_price_data = {
#     'Item': {
#         'SKU': '00161234',
#         'InventoryTrackingMethod': 'SKU',
#         'ConditionID': '1000',
#         'ListingDuration': 'GTC',
#         'Currency': 'USD',
#         'Country': 'US',
#         'PrimaryCategory': {'CategoryID': '63869'},
#         'Location': 'US',
#         'Title': 'This Girl Loves the 4th of July Juniors Soft Tank Top',
#         'Description': 'This Girl Loves the 4th of July Juniors Soft Tank Top',
#         'PaymentMethods': ['PayPal', 'CreditCard'],
#         'PayPalEmailAddress': 'payments@webfillment.com',
#         'DispatchTimeMax': '1',
#         'ItemSpecifics': {'NameValueList': [
#             {'Name': 'Size Type', 'Value': 'Regular'}, {'Name': 'Brand', 'Value': 'Old Glory'}, {'Name': 'Style', 'Value': 'Graphic Tee'}
#         ]},
#         'PictureDetails': {
#             'PictureURL': 'http://images.oldglory.com/product/00160025-NVYf.jpg',
#         },
#         'ReturnPolicy': {
#             'ReturnsAcceptedOption': 'ReturnsAccepted',
#             'RefundOption': 'MoneyBack',
#             'ReturnWithinOption': 'Days_30',
#         },
#         'ShippingDetails': {
#             'ShippingServiceOptions': [
#                 {
#                     'ShippingServicePriority': '1',
#                     'ShippingService': 'ShippingMethodStandard',
#                     'ShippingServiceCost': '5.95',
#                     'ShippingServiceAdditionalCost': '1.00',
#                 },
#                 {
#                     'ShippingServicePriority': '2',
#                     'ShippingService': 'UPS2ndDay',
#                     'ShippingServiceCost': '13.95',
#                     'ShippingServiceAdditionalCost': '1.00',
#                 },
#                 {
#                     'ShippingServicePriority': '3',
#                     'ShippingService': 'UPSNextDay',
#                     'ShippingServiceCost': '25.95',
#                     'ShippingServiceAdditionalCost': '1.00',
#                 },
#             ]
#         },
#          'Variations': {
#               'Pictures': {
#                   'VariationSpecificName': 'Colour',
#                   'VariationSpecificPictureSet':[
#                       {'PictureURL':'http://images.oldglory.com/product/00160025-BLKf.jpg', 'VariationSpecificValue': 'Black'},
#                       {'PictureURL':'http://images.oldglory.com/product/00160025-WHTf.jpg', 'VariationSpecificValue': 'White'},
#                       {'PictureURL':'http://images.oldglory.com/product/00160025-HTHf.jpg', 'VariationSpecificValue': 'Grey'},
#                       {'PictureURL':'http://images.oldglory.com/product/00160025-NVYf.jpg', 'VariationSpecificValue': 'Navy'},
#                   ]
#               },
#               'Variation': [
#                    {'Quantity': '1',
#                     'SKU': '00160025-BLK-MD',
#                     'InventoryTrackingMethod': 'SKU',
#                     'StartPrice': '25.95',
#                     'VariationProductListingDetails': {'UPC': '190345404875'},
#                     'VariationSpecifics': {'NameValueList': [{'Name': "Colour",
#                                                              'Value': 'Black'},
#                                                              {'Name': "Size (Men's)",
#                                                               'Value': "MD"}]}},
#                    {'Quantity': '1',
#                     'SKU': '00160025-WHT-SM',
#                     'InventoryTrackingMethod': 'SKU',
#                     'StartPrice': '25.95',
#                     'VariationProductListingDetails': {'UPC': '190345405018'},
#                     'VariationSpecifics': {'NameValueList': [{'Name': "Colour",
#                                                              'Value': 'White'},
#                                                             {'Name': "Size (Men's)",
#                                                              'Value': "SM"}]}},
#              ],
#              'VariationSpecificsSet': {'NameValueList': [{'Name': "Colour",
#                                                         'Value': ['White', 'Black', 'Navy', 'Grey']},
#                                                         {"Name": "Size (Men's)",
#                                                          'Value': ['SM', 'MD']}]},
#
#
#         }
#
#     }
# }
# r = api.revise_fixed_price_item(fixed_price_data)
# print r.dict()
import pprint
pprint.pprint(items)
