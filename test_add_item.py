from ebay_api import EbayAPI


# video_game_category = '139973'
# 
# fixed_price_data = {
#     'Item': {
#         'ListingDuration': 'Days_30',
#         'Quantity': '10',
#         'StartPrice': '1.01',
#         'Currency': 'USD',
#         'Country': 'US',
#         'ConditionID': '5000',
#         'PrimaryCategory': {'CategoryID': video_game_category},
#         'Location': 'US',
#         'Title': 'Metroid',
#         'Description': 'Metroid NES Cartridge',
#         'PaymentMethods': 'PayPal',
#         'PayPalEmailAddress': 'paul.mouzas@gmail.com',
#         'DispatchTimeMax': '3',
#         'ReturnPolicy': {
#             'ReturnsAcceptedOption': 'ReturnsAccepted',
#             'RefundOption': 'MoneyBack',
#             'ReturnWithinOption': 'Days_30',
#         },
#         'ShippingDetails': {
#             'ShippingServiceOptions': {
#                 'ShippingServicePriority': '1',
#                 'ShippingService': 'UPSGround',
#                 'ShippingServiceCost': '0.00',
#                 'ShippingServiceAdditionalCost': '0.00',
#             }
#         }
#     }
# }
# 
# ebay_api = EbayAPI()
# response = ebay_api.add_fixed_price_item(fixed_price_data)
# print response
# print(response.dict())
# print(response.reply)

shirt_category = '147340'

variation_item_data = {
    'Item': {
        'ListingDuration': 'Days_30',
        'InventoryTrackingMethod': 'SKU',
        'SKU': '1970',
        'Currency': 'USD',
        'Country': 'US',
        'ConditionID': '1000', # new
        'PrimaryCategory': {'CategoryID': shirt_category},
        'Location': 'US',
        'Title': 'Some weird shirt',
        'Description': 'Some weird shirt',
        'PaymentMethods': 'PayPal',
        'PayPalEmailAddress': 'paulm7224@yahoo.com',
        'DispatchTimeMax': '3',
        'ReturnPolicy': {
            'ReturnsAcceptedOption': 'ReturnsAccepted',
            'RefundOption': 'MoneyBack',
            'ReturnWithinOption': 'Days_30',
        },
        'ShippingDetails': {
            'ShippingServiceOptions': {
                'ShippingServicePriority': '1',
                'ShippingService': 'UPSGround',
                'ShippingServiceCost': '0.00',
                'ShippingServiceAdditionalCost': '0.00',
            }
        },
        'Variations': {
            'Variation': {
                'Quantity': '5',
                'SKU': '1970-XL',
                'StartPrice': '9.95',
                'VariationSpecifics': {
                    'NameValueList': {
                        'Name': 'Size',
                        'Value': 'XL',
                    }
                }
            },
            'Variation': {
                'Quantity': '9',
                'SKU': '1970-L',
                'StartPrice': '9.95',
                'VariationSpecifics': {
                    'NameValueList': {
                        'Name': 'Size',
                        'Value': 'L',
                    }
                }
            },
            'VariationSpecificsSet': {
                'NameValueList': {
                    'Name': 'Size',
                    'Value': 'XL',
                    'Value': 'L',
                }
            },
        } 
    }
}

ebay_api = EbayAPI()
response = ebay_api.add_fixed_price_item(variation_item_data)
print response.dict()
