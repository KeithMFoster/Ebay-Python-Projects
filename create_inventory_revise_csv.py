import os
import sys
import csv
import MySQLdb
from MySQLdb.cursors import DictCursor

storefront = sys.argv[1]

if storefront not in ('animalworld', 'old_glory'):
    print 'Invalid storefront.'
    sys.exit(1)


db = 'redrocket'
host = '10.1.10.28'
user = os.environ['MYSQLDB_USER']
passwd = os.environ['MYSQLDB_PASSWD']

conn = MySQLdb.Connect(db=db, user=user, passwd=passwd, host=host,
        charset='utf8', cursorclass=DictCursor)

print 'connected'
query = """
SELECT DISTINCT p.parentsku, p.parentchild
FROM producttable p
JOIN ebay_revise_table ert on ert.customlabel = p.sku
WHERE ert.pt_quantity != p.quantity
AND (p.parentchild = 'child' OR p.parentchild = 'lone')
AND p.storefront = %s;
"""

# query = """
# SELECT DISTINCT p.parentsku, p.parentchild
# FROM producttable p
# JOIN ebay_revise_table ert on ert.customlabel = p.sku
# WHERE (p.parentchild = 'child' OR p.parentchild = 'lone')
# AND p.storefront = %s
# limit 500;
# """

cursor = conn.cursor()
nrows = cursor.execute(query, (storefront,))
if not nrows:
    print 'Nothing to update...'
    sys.exit(0)

results = cursor.fetchall()

header = (
        "Action(SiteID=US|Country=US|Currency=USD|Version=585|CC=ISO-8859-1)",
        "ItemID", "Title", "SiteID", "Currency", "StartPrice", "BuyItNowPrice",
        "Quantity", "Relationship", "RelationshipDetails", "CustomLabel", "OutOfStockControl"
    )

f = open("%s_revise_file.csv" % (storefront,), 'w')
writer = csv.writer(f)
writer.writerow(header)
# results = list(results)
# results.sort(key=lambda x: x['sku'])


for j, result in enumerate(results):
    print j

    parentsku = result['parentsku']
    parentchild = result['parentchild']

    if parentchild == 'child':

        query = """SELECT (SELECT itemid FROM ebay_revise_table WHERE customlabel = p.parentsku LIMIT 1) AS 'parentitemid',
        (SELECT relationshipdetails FROM ebaycategorycrossref WHERE (bizcategory = p.primaryproductcategory AND department = p.department) LIMIT 1) as 'relationshipdetails',
        p.sku, ert.itemid, p.productname, price.itemprice, p.parentsku, p.parentchild,
        p.quantity, p.productstatus, p.producttype, p.department, id_code
        FROM producttable p
        JOIN pricingtable price on price.sku = p.sku
        JOIN ebay_revise_table ert on ert.customlabel = p.sku
        where p.sku like %s;
        """
        cursor = conn.cursor()
        cursor.execute(query, (parentsku + '-%',))
        children = cursor.fetchall()
        cursor.close()
        for i, child in enumerate(children):
            sku = child['sku']
            itemid = child['itemid']
            productname = child['productname'].encode('utf8')
            price = child['itemprice']
            quantity = child['quantity']
            parentsku = child['parentsku']
            parentchild = child['parentchild'].lower()
            parentitemid = child['parentitemid']
            relationshipdetails = child['relationshipdetails']
            department = child['department']
            id_code = child['id_code']
            producttype = child['producttype']


            if not relationshipdetails:
                relationshipdetails = ''
            if i == 0:
                # write the parent row
                sizes = ';'.join([e['id_code'] for e in children])
                csv_row = ['Revise', parentitemid, productname, 'US', 'USD',
                        '', '', '' , '', relationshipdetails + sizes, parentsku]
                writer.writerow(csv_row)

            if producttype != 'FINISHED_GOOD':
                ebay_quantity = 5
            else:
                if quantity < 10:
                    if quantity < 5:
                        ebay_quantity = 0
                    else:
                        ebay_quantity = quantity
                else:
                    ebay_quantity = 10

            outofstock = ''


            child_row = [
                    '', '', '', '', '', price, '',
                    ebay_quantity, 'Variation', relationshipdetails + id_code, sku, outofstock
                ]
            writer.writerow(child_row)

    elif parentchild == 'lone':
        query = """SELECT (SELECT itemid FROM ebay_revise_table WHERE customlabel = p.parentsku LIMIT 1) AS 'parentitemid',
        (SELECT relationshipdetails FROM ebaycategorycrossref WHERE (bizcategory = p.primaryproductcategory AND department = p.department) LIMIT 1) as 'relationshipdetails',
        p.sku, ert.itemid, p.productname, price.itemprice, p.parentsku, p.parentchild,
        p.quantity, p.productstatus, p.producttype, p.department, id_code
        FROM producttable p
        JOIN pricingtable price on price.sku = p.sku
        JOIN ebay_revise_table ert on ert.customlabel = p.sku
        WHERE p.sku = %s;
        """
        cursor = conn.cursor()
        cursor.execute(query, (parentsku,))
        lone = cursor.fetchone()
        cursor.close()

        sku = lone['sku']
        itemid = lone['itemid']
        productname = lone['productname'].encode('utf8')
        price = lone['itemprice']
        quantity = lone['quantity']
        parentsku = lone['parentsku']
        parentchild = lone['parentchild'].lower()
        parentitemid = lone['parentitemid']
        relationshipdetails = lone['relationshipdetails']
        department = lone['department']
        id_code = lone['id_code']

        producttype = lone['producttype']

        if producttype != 'FINISHED_GOOD':
            ebay_quantity = 5
        else:
            if quantity < 10:
                if quantity < 5:
                    ebay_quantity = 0
                else:
                    ebay_quantity = quantity
            else:
                ebay_quantity = 10

        if ebay_quantity == 0:
            outofstock = 'true'
        else:
            outofstock = ''
        lone_row = [
            'Revise', itemid, productname, 'US', 'USD', price,
            '', ebay_quantity, '', '', sku, outofstock]
        writer.writerow(lone_row)
