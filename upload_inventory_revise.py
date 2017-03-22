import os
import sys
import csv
import requests


def write_to_csv(fname, rows):
    '''Writes the data in rows to a file named fname.
    Will truncate the data in fname first'''
    header = (
            "Action(SiteID=US|Country=US|Currency=USD|Version=585|CC=ISO-8859-1)",
            "ItemID", "Title", "SiteID", "Currency", "StartPrice", "BuyItNowPrice", "Quantity",
            "Relationship", "RelationshipDetails", "CustomLabel"
        )

    with open(fname, 'wb+') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            new_row = [x.encode('utf8') for x in row]
            writer.writerow(new_row)

def main(key, storefront):

    # post csv revise file to this url
    url = "https://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchangeUpload"

    # # filename
    upload_file_name = '%s_revise_file.csv' % (storefront,)
    upload_file_name = 'animalworld_revise_file.csv'

    # # db connection data
    # user = 'root'
    # passwd = 'root'
    # host = os.environ.get("MYSQLDB_HOST")
    # db = 'redrocket'

    # # create connection to db
    # conn = MySQLdb.Connect(user=user, passwd=passwd, host=host, db=db, charset="utf8")
    # conn.query('SET GLOBAL connect_timeout=288000')
    # conn.query('SET GLOBAL wait_timeout=288000')
    # conn.query('SET GLOBAL interactive_timeout=288000')
    # cursor = conn.cursor()

    # # call the stored procedure with storefront as argument
    # cursor.callproc('Ebay_Revise_Builder', (storefront,))

    # # get results from stored procedure
    # results = cursor.fetchall()

    # print "%d rows fetched." % len(results)

    # # write data to csv file
    # write_to_csv(upload_file_name, results)

    url = "http://localhost:8000"
    filedata = open(upload_file_name, "r")
    files = {"file": (upload_file_name, filedata, "text/csv"), "token": ('', key)}
    r = requests.post(url, files=files)

    print r.status_code
    print r.text


if __name__ == '__main__':
    STOREFRONTS = ['animalworld', 'old_glory']
    storefront = sys.argv[1]
    if storefront not in STOREFRONTS:
        print 'Incorrect storefront...'
        sys.exit(1)

    if storefront.lower() == 'animalworld':
        key = os.environ.get('AW_EBAY_TOKEN')
        # key = "AgAAAA**AQAAAA**aAAAAA**A5eUVA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFlYKnAZOApwidj6x9nY+seQ**qKgBAA**AAMAAA**0Y2RTfVifoo2s/nyLFlX5xMUIWPBKd3MJHloaxLhnVnOTjfJ7ZLR9hPfL87HbKQxR1XsFEf4kXHqKGfNow7dHYimjhtY9CVhbeVFpBPFK0NxY4xEZRcrc/W212Vry1Gw1LHi9xLD6PjYlek6OLqDfbv/+oi3C9H7dbozPuLbQoLKHYczACFOwpV64wGmG7DfndAM5aZwLWV3w4h8CSRnQZ5NZDoWdVi0pZLn48ntwQfT2uTkvlmqYiHBOSpfvT6Y7lxzbVlB88n5BHh/5Br5Ws1i+xqQ7tcWtGSsPv+qzl2N2mxMm+FEB3J1UkksEHuzoiZV5h9gfe4YqA+H2CuA/0vGufoBqWJ8O1qcDYplifah4i58xGMugEN6OYa2AKnnWDEZQLUYWtMOcC0vz3hCPLfZi2b6J/CodeQdjjqEcyqLJZ6GBr+yVsmbaFnOzmLpBtKIVupxiW5YkzCBVy4RCw/F9sc7dNxYpl1GVGeLKA/yFjhoX8vQCOg8coneQ5nTbE9yDFxzV+2cjYmVmfeHEjps0kQEZV2O9Xf1VBC2hj2Di8mnDtY+C5lNSCzqJ+RQ8SmLh7+7uJ0gOCsU4okNzVQMm1xVWcW9lmBxZy5X0/LZyI31cDCFgyghedxexpErmfCPlDMf+KCCJGXBGEdULU0pUOL+AIznTdSThhyEPxXaNN8jcv5qb7WbjxW2MB5VzVZgUfHgIvtyxYh35I1Yt6p5MQacCYdoa1anhHeeGSDZ/goggKze7s28RM7g5uct"
    elif storefront.lower() == 'old_glory':
        key = os.environ.get('OG_EBAY_TOKEN')
        # key = "AgAAAA**AQAAAA**aAAAAA**jR1aVQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFmYSkDpWKogidj6x9nY+seQ**qKgBAA**AAMAAA**DZ+zRIFhLgcfppoWNyZf8oZzdRDB10Pw8IN0S+uwseDmY7mYqLWdYod8VUjhTHsg0Dt9XfGtN7YjO9Az2a2pRXw9OfYI3uKGGFMiPdmJhU8TCFmJo86kxZIbXVEw/byRFta8EbECGS3uV0Xy7XuXEMaYk68q9QXG9l8TV6j8tXABuSIwZpV4Crxfj/GYOgNEeo9ABTqldgAj5o72og0EVCNo5vEg1ovyn1KC/AddHSacXLG3XBSiYiE2OtF5iMM8gGq/blk9NGJw1HFLVglTMK5b4NhjFq/cLTSkLs+LIKkRjQuGK6NQumQVp7LmouJoox54eGDjp5dnW+DdzfhSAhaC/60ZippcJIaWnqpWSUKxJAAyJEsZHWOhLlvie1gVukx3sB8HBtJ+u/+6XhMK7CZ2Pw+xeVMeY2wo78FXbh1oELpBir+KYkg1+wO4LgMDUQItSXwoejyhIrJ/bY7QEk7YdfzkFoyUz/6LPd9tC2JwIIcaVPxAB8uWIVwfpkGik/8jBb/+0SbRv1aXRmSaZN8znks3hygnmi0LB18ahLZDRHFfY/4X8U5r5Cbs8rV48qTtYM/F2C3Sv9Yc7ZAV5H8vo+kXNoDfcaoEuBZAfTZhtF2q6gxtCjIKLX/2dKmr570HV8OdNmKBIg6zgTF5HxH9VXsIKfqcYOFL69iQ+RD8gHePPHRUPsavxja12z6wchdKKHC/JQIVNsx7nLLwm2apiCl0A4rEhsKNnWTC90d0VRuRMeCeNPd+jU+nwZvQ"

    main(key, storefront)

