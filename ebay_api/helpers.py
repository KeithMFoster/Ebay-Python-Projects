from lxml.etree import Element, SubElement, tostring
from ebay_api import EbayAPI
from iMerchandise.connection import iMerchConnection
from itertools import groupby
import csv
import os
import StringIO
import gzip

def create_ebay_revise_csv(storefront_id):
    query = """
SELECT IF(ps.ebay_parent_child = 'parent'
           OR ps.ebay_parent_child = 'lone', 'Revise', '')                    AS
       'Action(SiteID=US|Country=US|Currency=USD|Version=585|CC=ISO-8859-1)',
       ps.item_id                                                             AS
       'ItemID',
       p.sku                                                                  AS
       'CustomLabel',
       IF(ps.ebay_parent_child = 'child', Concat(ps.name, '=', ps.value), if(ps.ebay_parent_child = 'lone', '', concat((select e2.name from ebay_inventory e2 join product p2 on p2.sku = e2.sku where e2.sku = p2.sku and p2.parentchild <> 'parent' and p2.parentsku = p.sku limit 1),'=', (select group_concat(e.value separator ';') from redrocket.ebay_inventory e join product p2 on p2.sku = e.sku where p2.parentsku = p.sku and p2.sku <> p.parentsku )) )) AS
       RelationshipDetails,
       IF(ps.ebay_parent_child = 'child', 'Variation', '')                    AS
       Relationship,
       IF(ps.ebay_parent_child = 'parent', '',
       IF(p.productstatus = 'R1', IF(
                                  IF(pi.virtual_stock_allowed = 'Y',
                                  pi.virtual_quantity, pi.quantity) <= (SELECT
                                  IF(r1_enabled = 1, r1_limit, 9999)
                                     FROM
                                  feedersettings.threshold_settings
                                     WHERE  channel_id = 4
                                            AND storefront_id = 1), 0,
       IF(pi.virtual_stock_allowed = 'Y',
                                  IF(pi.virtual_quantity > 5, 5,
                                  pi.virtual_quantity),
                                  IF(pi.quantity > 5, 5, pi.quantity))),
       IF(
       IF(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.quantity) <= (
       SELECT
       IF(c1_enabled = 1, c1_limit, 9999)
           FROM
       feedersettings.threshold_settings
           WHERE  channel_id = 4
                  AND storefront_id = 1), 0,
       IF(pi.virtual_stock_allowed = 'Y',
                                             IF(
       pi.virtual_quantity > 5, 5, pi.virtual_quantity),
       IF(pi.quantity > 10, 10, pi.quantity)))))
                                        AS 'Quantity'
FROM   redrocket.ebay_inventory AS ps
       INNER JOIN redrocket.product_inventory AS pi
               ON ps.sku = pi.sku
       INNER JOIN redrocket.product AS p
               ON ps.sku = p.sku
       INNER JOIN redrocket.product_stores AS product_stores
               ON product_stores.sku = ps.sku
WHERE  ps.on_ebay > 0
       AND product_stores.storefront_id = 1 ORDER  BY p.sku;  """
    conn = iMerchConnection()
    conn.cursor.execute(query, (storefront_id,))
    results = conn.cursor.fetchall()
    f = StringIO.StringIO()
    writer = csv.DictWriter(f, fieldnames=['Action', 'ItemID','Relationship', 'CustomLabel', 'RelationshipDetails', 'Quantity'])
    writer.writeheader()
    writer.writerows(results)
    f.seek(0)
    return f



def get_ebay_inventory_old(storefront_id):
    query = """
    select p.parentsku, ps.sku, pi.quantity as `actual_quantity`, ps.name, ps.value, ps.ebay_parent_child, ps.item_id, p.producttype, pi.virtual_stock_allowed,
    if(p.productstatus = 'R1',
        if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(r1_enabled = 1, r1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = %(storefront_id)s), 0, if(pi.virtual_stock_allowed = 'Y', if(pi.virtual_quantity > 5, 5, pi.virtual_quantity), if(pi.quantity > 5, 5, pi.quantity))) ,
        if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(c1_enabled = 1, c1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = %(storefront_id)s), 0, if(pi.virtual_stock_allowed = 'Y', if(pi.virtual_quantity > 5, 5, pi.virtual_quantity), if(pi.quantity > 10, 10, pi.quantity)))) as quantity,
    pi.InventoryUpdate
    from redrocket.ebay_inventory as ps
    inner join redrocket.product_inventory as pi on ps.sku = pi.sku
    inner join redrocket.product as p on ps.sku = p.sku
    inner join redrocket.product_stores as product_stores on product_stores.sku = ps.sku
    # where ps.on_ebay > 0
    where ps.ebay_parent_child <> 'parent'
    and product_stores.storefront_id = %(storefront_id)s
    order by p.parentsku
    """
    conn = iMerchConnection()
    conn.cursor.execute(query, {'storefront_id': storefront_id})
    results = conn.cursor.fetchall()
    return results

def get_ebay_inventory(storefront):
    query = """
    select pi.virtual_quantity, pi.virtual_stock_allowed, pi.quantity as `actual_quantity`, ps.name, ps.value, ps.sku, ps.parent_sku, ps.item_id, p.producttype, pi.virtual_stock_allowed,
    if(p.productstatus = 'R1',
        if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(r1_enabled = 1, r1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = 1), 0, if(pi.virtual_stock_allowed = 'Y', if(pi.virtual_quantity > 5, 5, pi.virtual_quantity), if(pi.quantity > 5, 5, pi.quantity))) ,
        if(if(pi.virtual_stock_allowed = 'Y', pi.virtual_quantity, pi.Quantity) <= (select if(c1_enabled = 1, c1_limit, 9999) from feedersettings.threshold_settings where channel_id = 4 and storefront_id = 1), 0, if(pi.virtual_stock_allowed = 'Y', if(pi.virtual_quantity > 5, 5, pi.virtual_quantity), if(pi.quantity > 10, 10, pi.quantity)))) as quantity,
    pi.InventoryUpdate
    from redrocket.ebay_inventory_2 as ps
    inner join redrocket.product_inventory as pi on ps.sku = pi.sku
    inner join redrocket.product as p on ps.sku = p.sku
    where ps.storefront = %s
    # where ps.on_ebay > 0
    # where ps.ebay_parent_child <> 'parent'
    order by ps.item_id;
    """
    conn = iMerchConnection()
    conn.cursor.execute(query, (storefront,))
    results = conn.cursor.fetchall()
    return results

# item = {
#     'Item': {
#         'ItemID': item_id,
#         'SKU': sku,
#         'Variations': {
#             'Variation': {
#                 'SKU': sku,
#                 'VariationSpecifics': {
#                     'NameValueList': {
#                         'Name': name,
#                         'Value': value,
#                     }
#                 }
#             },
#         }
#     }
# }

def create_ebay_revise_xml_file_old(storefront_id):
    data = get_ebay_inventory(storefront_id)

    bulk_data_exchange = Element('BulkDataExchangeRequests', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
    header = SubElement(bulk_data_exchange, 'Header')
    version = SubElement(header, 'Version')
    version.text = '583'
    site_id = SubElement(header, 'SiteID')
    site_id.text = '0'
    for parent_sku, group in groupby(data, key=lambda x: x['parentsku']):
        variations = list(group)

        revise_fixed_price_item_request = SubElement(bulk_data_exchange, 'ReviseFixedPriceItemRequest', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
        error_lang_el = SubElement(revise_fixed_price_item_request, 'ErrorLanguage')
        error_lang_el.text = 'en_us'

        version_el = SubElement(revise_fixed_price_item_request, 'Version')
        version_el.text = '583'

        item_el = SubElement(revise_fixed_price_item_request, 'Item')
        item_id_el = SubElement(item_el, 'ItemID')
        item_id_el.text = variations[0]['item_id']
        if variations[0]['ebay_parent_child'] == 'lone':
            sku_el = SubElement(item_el, 'SKU')
            sku_el.text = variations[0]['sku']
            sku_el = SubElement(item_el, 'Quantity')
            sku_el.text = str(variations[0]['quantity'])
            continue

        variations_el = SubElement(item_el, 'Variations')
        for variation in variations:
            variation_el = SubElement(variations_el, 'Variation')
            sku_el = SubElement(variation_el, 'SKU')
            sku_el.text = variation['sku']

            sku_el = SubElement(variation_el, 'Quantity')
            sku_el.text = str(variation['quantity'])

            variation_specifics_el = SubElement(variation_el, 'VariationSpecifics')
            name_value_list_el = SubElement(variation_specifics_el, 'NameValueList')
            name_el = SubElement(name_value_list_el, 'Name')
            name_el.text = variation['name']

            value_el = SubElement(name_value_list_el, 'Value')
            value_el.text = variation['value']
    return tostring(bulk_data_exchange, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def create_ebay_revise_xml_file(storefront):
    data = get_ebay_inventory(storefront)

    bulk_data_exchange = Element('BulkDataExchangeRequests', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
    header = SubElement(bulk_data_exchange, 'Header')
    version = SubElement(header, 'Version')
    version.text = '583'
    site_id = SubElement(header, 'SiteID')
    site_id.text = '0'
    for parent_sku, group in groupby(data, key=lambda x: x['item_id']):
        variations = list(group)

        revise_fixed_price_item_request = SubElement(bulk_data_exchange, 'ReviseFixedPriceItemRequest', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
        error_lang_el = SubElement(revise_fixed_price_item_request, 'ErrorLanguage')
        error_lang_el.text = 'en_us'

        version_el = SubElement(revise_fixed_price_item_request, 'Version')
        version_el.text = '583'

        item_el = SubElement(revise_fixed_price_item_request, 'Item')
        item_id_el = SubElement(item_el, 'ItemID')
        item_id_el.text = variations[0]['item_id']
        if variations[0]['sku'] == variations[0]['parent_sku']:
            quantity_el = SubElement(item_el, 'Quantity')
            quantity_el.text = str(variations[0]['quantity'])
            continue

        variations_el = SubElement(item_el, 'Variations')
        for variation in variations:
            variation_el = SubElement(variations_el, 'Variation')

            quantity_el = SubElement(variation_el, 'Quantity')
            quantity_el.text = str(variation['quantity'])

            variation_specifics_el = SubElement(variation_el, 'VariationSpecifics')
            name_value_list_el = SubElement(variation_specifics_el, 'NameValueList')
            name_el = SubElement(name_value_list_el, 'Name')
            name_el.text = variation['name']

            value_el = SubElement(name_value_list_el, 'Value')
            value_el.text = variation['value']
    return tostring(bulk_data_exchange, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def create_relist_xml_from_item_ids(item_ids):

    bulk_data_exchange = Element('BulkDataExchangeRequests', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
    header = SubElement(bulk_data_exchange, 'Header')
    version = SubElement(header, 'Version')
    version.text = '583'
    site_id = SubElement(header, 'SiteID')
    site_id.text = '0'
    for item_id in item_ids:

        revise_fixed_price_item_request = SubElement(bulk_data_exchange, 'RelistFixedPriceItemRequest', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
        error_lang_el = SubElement(revise_fixed_price_item_request, 'ErrorLanguage')
        error_lang_el.text = 'en_us'

        version_el = SubElement(revise_fixed_price_item_request, 'Version')
        version_el.text = '583'

        item_el = SubElement(revise_fixed_price_item_request, 'Item')
        item_id_el = SubElement(item_el, 'ItemID')
        item_id_el.text = str(item_id)
    return tostring(bulk_data_exchange, pretty_print=True, xml_declaration=True, encoding='UTF-8')

# def create_ebay_revise_xml(data):
#
#     bulk_data_exchange = Element('BulkDataExchangeRequests', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
#     header = SubElement(bulk_data_exchange, 'Header')
#     version = SubElement(header, 'Version')
#     version.text = '583'
#     site_id = SubElement(header, 'SiteID')
#     site_id.text = '0'
#     for item in data:
#         revise_fixed_price_item_request = SubElement(bulk_data_exchange, 'ReviseFixedPriceItemRequest', attrib={'xmlns': 'urn:ebay:apis:eBLBaseComponents'})
#         error_lang_el = SubElement(revise_fixed_price_item_request, 'ErrorLanguage')
#         error_lang_el.text = 'en_us'
#
#         version_el = SubElement(revise_fixed_price_item_request, 'Version')
#         version_el.text = '583'
#
#         item_el = SubElement(revise_fixed_price_item_request, 'Item')
#         item_id_el = SubElement(item_el, 'ItemID')
#         item_id_el.text = item['Item']['ItemID']
#
#         variations = item['Item'].get('Variations')
#         if type(variations) == dict:
#             variations = [item['Item']['Variations']]
#         elif variations is None:
#             sku_el = SubElement(item_el, 'SKU')
#             sku_el.text = item['Item']['SKU']
#             sku_el = SubElement(item_el, 'Quantity')
#             sku_el.text = str(item['Item']['Quantity'])
#             continue
#
#         else:
#             pass
#
#         variations_el = SubElement(item_el, 'Variations')
#         for variation in variations:
#             variation_el = SubElement(variations_el, 'Variation')
#             sku_el = SubElement(variation_el, 'SKU')
#             sku_el.text = variation['Variation']['SKU']
#
#             sku_el = SubElement(variation_el, 'Quantity')
#             sku_el.text = str(variation['Variation']['Quantity'])
#
#             variation_specifics_el = SubElement(variation_el, 'VariationSpecifics')
#             name_value_list_el = SubElement(variation_specifics_el, 'NameValueList')
#             name_el = SubElement(name_value_list_el, 'Name')
#             name_el.text = variation['Variation']['VariationSpecifics']['NameValueList']['Name']
#
#             value_el = SubElement(name_value_list_el, 'Value')
#             value_el.text = variation['Variation']['VariationSpecifics']['NameValueList']['Value']
#     return tostring(bulk_data_exchange, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def get_all_upload_jobs():
    api = EbayAPI('old_glory')
    api.get_all_created_jobs()

def create_inventory_dicts(inventories):
    items = []
    for parent, group in groupby(inventories, key=lambda x: x['item_id']):
        item = {'Item': {'Variations': []}}
        for child in group:
            if child['ebay_parent_child'] == 'lone':
                item = {
                    'Item': {
                        'ItemID': child['item_id'],
                        'SKU': child['sku'],
                        'Quantity': child['quantity']
                    }
                }
                items.append(item)
                break
            else:
                variation = {'Variation': {}}
                variation['Variation']['SKU'] = child['sku']
                variation['Variation']['Quantity'] = child['quantity']
                variation['Variation']['VariationSpecifics'] = {'NameValueList': {}}
                variation['Variation']['VariationSpecifics']['NameValueList']['Name'] = child['name']
                variation['Variation']['VariationSpecifics']['NameValueList']['Value'] = child['value']
                item['Item']['Variations'].append(variation)

            item['Item']['ItemID'] = child['item_id']
            items.append(item)
    return items

if __name__ == '__main__':
    # xml = create_ebay_revise_xml_file(1)

    # with open('ebay_inventory.xml', 'w') as f:
    #     f.write(xml)
    import ebay_api

    # item = {
    #     'Item': {
    #         'ItemID': '141616010649',
    #         # 'SKU': sku,
    #         'Variations': [
    #             {
    #                 'Variation': {
    #                     'SKU': '24522-LG',
    #                     'Quantity': 7,
    #                     'VariationSpecifics': {
    #                         'NameValueList': {
    #                             'Name': "Size (Women's)",
    #                             'Value': 'LG',
    #                         }
    #                     }
    #                 }
    #             },
    #             {
    #                 'Variation': {
    #                     'SKU': '24522-XL',
    #                     'Quantity': 10,
    #                     'VariationSpecifics': {
    #                         'NameValueList': {
    #                             'Name': "Size (Women's)",
    #                             'Value': 'XL',
    #                         }
    #                     }
    #                 }
    #             }
    #         ]
    #     }
    # }
    # import pprint
    # api = ebay_api.EbayAPI('old_glory')
    # storefront_id = 1
    # inventories = get_ebay_inventory(storefront_id)
    # i = create_inventory_dicts(inventories)
    # pprint.pprint(i)
    # with open('inventory.xml', 'w') as f:
    #     xml = create_ebay_revise_xml(i)
    #     f.write(xml)
    # xml = create_ebay_revise_xml([item])
    # print xml
    # # with open('inventory.xml', 'w') as f:
    # #     f.write(xml)
    # xml = open('ebay_inventory.xml')
    # xml = xml.read()
    api = ebay_api.EbayAPI('old_glory')
    # with gzip.open('inventory.xml.gz', 'w') as f:
    #     f.write(xml)

    # response = api.create_upload_job_for_revise_fixed_price_item()
    # file_reference_id, job_id = response['file_reference_id'], response['job_id']

    # response = {'file_reference_id': '5875552124', 'job_id': '5791640134'}
    # file_reference_id, job_id = response['file_reference_id'], response['job_id']
    job_id = '5792700374'
    file_reference_id = '5876744754'
    api.upload_file_request(job_id, file_reference_id, 'inventory.xml.gz')
    api.start_upload_job(job_id)



