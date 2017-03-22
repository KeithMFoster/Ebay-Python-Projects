import random
import csv
import requests
import base64
import time
from StringIO import StringIO
from lxml import etree
from ebaysdk.trading import Connection as Trading
from iMerchandise.connection import iMerchConnection

# sandbox
sandbox_token = "AgAAAA**AQAAAA**aAAAAA**KzuQVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCZSFqQidj6x9nY+seQ**qvQBAA**AAMAAA**Jebog7KYn48syZiJMKQCPvvANPZJESCwEVz6cdTwUDm4h6Qs0PLkq5cszTlsMhufHc1HysSozdznvGFb2fv2l+oYS4+T/jkCMkzyGpTKL68dRYXTKROfyhDgzN8lGiSyMGaQOjAyNUlwDTCElNyN+6XcPcBkpjXvl2BzUYr/JaVQCcxVqT/uHQf/+531P8zhEDonatmxS2ZxzKLgj/dT3p419wzCC7juUx0ZBKuzt5GX6O7cZNgqK1UVTfh+IG6/ROoQCxwYrkX8XU7/dI3A4BZ98ZSFczOLxU9dM/w6anvQs0rlCPSoNNBaE+ZgWI9tWmkrLUDYMRsCxyNZdsJs9LD2SXfMkPCyl68WcH3UKCx1WrSb2mFVZVMiR/rwuK8OcKCeSFkZzrYkSKKCgIbh949X4ffz2CT5h97wgTXs3qPydPmAbHHvmZNZM+T9LY9wiHJGE8fe9LBQaq4hg8TSVRNJMQZNyA9/dPr1a8fxVsNLj7CsaX2Eh4veERdrOSKKUKKxdmtIpM5hF/BdqB3oED6bbm595hjgQj++ip+Qo6slsyQwcJ7rDQzdnutiGYmLuFae6TG2+uMWk7JrraJIpA7HTJZihJczPXH/W4IGP5Wknq2rEzfZp82j3YiiBSH0dTFcp4K3LA8RYfbzO6/FnnFUqvYfHlkmW0msbOnWCI/Ga5WdXAZXOD8Kj6qZchPxB7A+SYB3rXbFb1eaZYpsnZICQVXq144VOMU7b3r5n9FvSlBjH0q2QXh9h7hW6Ck0"
aw_token = r"AgAAAA**AQAAAA**aAAAAA**U7iYUg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFlYKnAZOApwidj6x9nY+seQ**qKgBAA**AAMAAA**0Y2RTfVifoo2s/nyLFlX5xMUIWPBKd3MJHloaxLhnVnOTjfJ7ZLR9hPfL87HbKQxR1XsFEf4kXHqKGfNow7dHYimjhtY9CVhbeVFpBPFK0NxY4xEZRcrc/W212Vry1Gw1LHi9xLD6PjYlek6OLqDfbv/+oi3C9H7dbozPuLbQoLKHYczACFOwpV64wGmG7DfndAM5aZwLWV3w4h8CSRnQZ5NZDoWdVi0pZLn48ntwQfT2uTkvlmqYiHBOSpfvT6Y7lxzbVlB88n5BHh/5Br5Ws1i+xqQ7tcWtGSsPv+qzl2N2mxMm+FEB3J1UkksEHuzoiZV5h9gfe4YqA+H2CuA/0vGufoBqWJ8O1qcDYplifah4i58xGMugEN6OYa2AKnnWDEZQLUYWtMOcC0vz3hCPLfZi2b6J/CodeQdjjqEcyqLJZ6GBr+yVsmbaFnOzmLpBtKIVupxiW5YkzCBVy4RCw/F9sc7dNxYpl1GVGeLKA/yFjhoX8vQCOg8coneQ5nTbE9yDFxzV+2cjYmVmfeHEjps0kQEZV2O9Xf1VBC2hj2Di8mnDtY+C5lNSCzqJ+RQ8SmLh7+7uJ0gOCsU4okNzVQMm1xVWcW9lmBxZy5X0/LZyI31cDCFgyghedxexpErmfCPlDMf+KCCJGXBGEdULU0pUOL+AIznTdSThhyEPxXaNN8jcv5qb7WbjxW2MB5VzVZgUfHgIvtyxYh35I1Yt6p5MQacCYdoa1anhHeeGSDZ/goggKze7s28RM7g5uct"
og_token = r"AgAAAA**AQAAAA**aAAAAA**jR1aVQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFmYSkDpWKogidj6x9nY+seQ**qKgBAA**AAMAAA**DZ+zRIFhLgcfppoWNyZf8oZzdRDB10Pw8IN0S+uwseDmY7mYqLWdYod8VUjhTHsg0Dt9XfGtN7YjO9Az2a2pRXw9OfYI3uKGGFMiPdmJhU8TCFmJo86kxZIbXVEw/byRFta8EbECGS3uV0Xy7XuXEMaYk68q9QXG9l8TV6j8tXABuSIwZpV4Crxfj/GYOgNEeo9ABTqldgAj5o72og0EVCNo5vEg1ovyn1KC/AddHSacXLG3XBSiYiE2OtF5iMM8gGq/blk9NGJw1HFLVglTMK5b4NhjFq/cLTSkLs+LIKkRjQuGK6NQumQVp7LmouJoox54eGDjp5dnW+DdzfhSAhaC/60ZippcJIaWnqpWSUKxJAAyJEsZHWOhLlvie1gVukx3sB8HBtJ+u/+6XhMK7CZ2Pw+xeVMeY2wo78FXbh1oELpBir+KYkg1+wO4LgMDUQItSXwoejyhIrJ/bY7QEk7YdfzkFoyUz/6LPd9tC2JwIIcaVPxAB8uWIVwfpkGik/8jBb/+0SbRv1aXRmSaZN8znks3hygnmi0LB18ahLZDRHFfY/4X8U5r5Cbs8rV48qTtYM/F2C3Sv9Yc7ZAV5H8vo+kXNoDfcaoEuBZAfTZhtF2q6gxtCjIKLX/2dKmr570HV8OdNmKBIg6zgTF5HxH9VXsIKfqcYOFL69iQ+RD8gHePPHRUPsavxja12z6wchdKKHC/JQIVNsx7nLLwm2apiCl0A4rEhsKNnWTC90d0VRuRMeCeNPd+jU+nwZvQ"

def get_ebay_inventory(storefront_id):
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


class EbayFileDownloadResponse(object):
    def __init__(self, response_file):

        # TODO
        # quick and dirty
        boundary = response_file.readline()
        while True:
            if response_file.readline() == '\r\n':
                break
        xml_lines = []
        while True:
            line = response_file.readline()
            if line == boundary:
                break
            xml_lines.append(line)
        xml_response = ''.join(xml_lines)
        nsmap = {'services': 'http://www.ebay.com/marketplace/services'}
        root = etree.fromstring(xml_response)
        size = int(root.find('.//services:Size', nsmap).text)
        while True:
            if response_file.readline() == '\r\n':
                break
        self.data = response_file.read(size)

    def write_file(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fname = timestr + ".zip"
        with open(fname, 'w') as f:
            f.write(self.data)
        return fname


class EbayAPI(object):
    def __init__(self, storefront):
        self.storefront = storefront
        if storefront == 'old_glory':
            self.token = og_token
        elif storefront == 'animalworld':
            self.token = aw_token
        else:
            self.token = sandbox_token

        self.api = Trading(# domain='api.sandbox.ebay.com',
               appid="RedRocke-e380-4b45-ba54-78fb6c6832f5",
               devid="f7e7239f-2cf9-4e4f-9413-1e08b524944c",
               certid="7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
               token=self.token, config_file=None)

    def create_active_ebay_inventory_file(self):
        fname = self.storefront + "_active_ebay_inventory.csv"
        f = open(fname, "w")
        writer = csv.writer(f)

        page_number = 1

        # TODO handle connection timeout error
        results = self.get_my_ebay_selling(page_number)
        results_dict = results.dict()
        total_number_of_pages = int(results_dict['ActiveList']['PaginationResult']['TotalNumberOfPages'])
        active_items_array = results_dict['ActiveList']['ItemArray']['Item']

        while page_number <= total_number_of_pages:
            print page_number

            for item in active_items_array:
                item_id = item['ItemID']
                quantity = item.get('Quantity', '')
                sku = item.get('SKU', '')

                try:
                    variations = item['Variations']['Variation']
                    # if there are variations then this is an ebay parent
                    writer.writerow([item_id, sku, quantity, '', '', 'parent'])
                except KeyError:
                    variations = None
                    # if there are no variations this is a lone
                    writer.writerow([item_id, sku, quantity, '', '', 'lone'])
                if variations:
                    if type(variations) is list:
                        for variation in variations:
                            var_sku = variation.get("SKU", '')
                            var_quantity = variation.get('Quantity', '')
                            name_value_list = variation['VariationSpecifics']['NameValueList']
                            name = name_value_list['Name']
                            value = name_value_list['Value']
                            writer.writerow([item_id, var_sku, var_quantity, name, value, 'child'])
                    else:
                        var_sku = variations.get('SKU', '')
                        var_quantity = variations.get('Quantity', '')
                        # name_value_list = variation['VariationSpecifics']['NameValueList']
                        # if type(name_value_list) is list:
                        #     for name_value in name_value_list:
                        #         name = name_value['Name']
                        #         value = name_value['Value']
                        #         writer.writerow([item_id, var_sku, var_quantity, name, value])
                        # else:
                        #     name = name_value_list['Name']
                        #     value = name_value_list['Value']
                        #     writer.writerow([item_id, var_sku, var_quantity, name, value])

                        name_value_list = variations['VariationSpecifics']['NameValueList']
                        name = name_value_list['Name']
                        value = name_value_list['Value']
                        writer.writerow([item_id, var_sku, var_quantity, name, value, 'child'])

            page_number += 1

            results = self.get_my_ebay_selling(page_number)
            results_dict = results.dict()
            total_number_of_pages = int(results_dict['ActiveList']['PaginationResult']['TotalNumberOfPages'])
            active_items_array = results_dict['ActiveList']['ItemArray']['Item']
        return fname


    def create_upload_job_for_revise_fixed_price_item(self, upload_job_type):
        '''
        :return: job id str
        '''

        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "createUploadJob",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '83t',
            "X-EBAY-API-APP-NAME": "RedRocke-e380-4b45-ba54-78fb6c6832f5",
            "X-EBAY-API-CALL-NAME": 'ReviseFixedPriceItem',
            'X-EBAY-API-DETAIL-LEVEL': '0',
            "X-EBAY-API-SITEID": '0',
            "X-EBAY-APE-CERT-NAME": "7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
            "X-EBAY-API-DEV-NAME": "f7e7239f-2cf9-4e4f-9413-1e08b524944c",
            "Content-Type": 'application/xml',
        }
        # url = "https://api.ebay.com/ws/api.dll"
        url = "https://webservices.ebay.com/BulkDataExchangeService"

        # ebay needs some unique identifier
        uuid = ''.join([random.choice('abcdef123456') for _ in range(12)])

        xml = """<?xml version="1.0" encoding="utf-8"?>
        <createUploadJobRequest xmlns="http://www.ebay.com/marketplace/services">
          <RequesterCredentials>
            <eBayAuthToken>{token}</eBayAuthToken>
          </RequesterCredentials>
          <fileType>XML</fileType>
          <uploadJobType>{upload_job_type}</uploadJobType>
          <UUID>{uuid}</UUID>
        </createUploadJobRequest>
        """.format(token=self.token, uuid=uuid, upload_job_type=upload_job_type)


        r = requests.post(url, headers=headers, data=xml)
        print 'Content', r.content

        nsmap = {'services': 'http://www.ebay.com/marketplace/services'}
        root = etree.fromstring(r.content)
        job_id = root.find('services:jobId', nsmap).text
        file_reference_id = root.find('services:fileReferenceId', nsmap).text

        return {'job_id': job_id, 'file_reference_id': file_reference_id}

    def create_active_inventory_report(self):
        '''
        :return: job id str
        '''

        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "startDownloadJob",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '83t',
            "X-EBAY-API-APP-NAME": "RedRocke-e380-4b45-ba54-78fb6c6832f5",
            "X-EBAY-API-CALL-NAME": 'ActiveInventoryReport',
            'X-EBAY-API-DETAIL-LEVEL': '0',
            "X-EBAY-API-SITEID": '0',
            "X-EBAY-APE-CERT-NAME": "7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
            "X-EBAY-API-DEV-NAME": "f7e7239f-2cf9-4e4f-9413-1e08b524944c",
            "Content-Type": 'application/xml',
        }
        # url = "https://api.ebay.com/ws/api.dll"
        url = "https://webservices.ebay.com/BulkDataExchangeService"

        # ebay needs some unique identifier
        uuid = ''.join([random.choice('abcdef123456') for _ in range(12)])

        xml = """<?xml version="1.0" encoding="utf-8"?>
        <startDownloadJobRequest xmlns="http://www.ebay.com/marketplace/services">
          <RequesterCredentials>
            <eBayAuthToken>{token}</eBayAuthToken>
          </RequesterCredentials>
          <ActiveList>
            <Sort>TimeLeft</Sort>
            <Pagination>
              <EntriesPerPage>50</EntriesPerPage>
              <PageNumber>1</PageNumber>
            </Pagination>
          </ActiveList>
          <UUID>{uuid}</UUID>
          <downloadJobType>ActiveInventoryReport</downloadJobType>
        </startDownloadJobRequest>
        """.format(token=self.token, uuid=uuid)


        r = requests.post(url, headers=headers, data=xml)
        print 'Content', r.content

        nsmap = {'services': 'http://www.ebay.com/marketplace/services'}
        root = etree.fromstring(r.content)
        job_id = root.find('services:jobId', nsmap).text

        return job_id

    def get_job_status_request(self, job_id):
        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "getJobStatus",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '837',
            "X-EBAY-API-APP-NAME": "RedRocke-e380-4b45-ba54-78fb6c6832f5",
            'X-EBAY-API-DETAIL-LEVEL': '0',
            "X-EBAY-API-SITEID": '0',
            "X-EBAY-APE-CERT-NAME": "7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
            "X-EBAY-API-DEV-NAME": "f7e7239f-2cf9-4e4f-9413-1e08b524944c",
            "Content-Type": 'application/xml',
        }
        # url = "https://api.ebay.com/ws/api.dll"
        url = "https://webservices.ebay.com/BulkDataExchangeService"

        xml = """<?xml version="1.0" encoding="utf-8"?>
        <getJobsStatusRequest xmlns="http://www.ebay.com/marketplace/services">
          <RequesterCredentials>
            <eBayAuthToken>{token}</eBayAuthToken>
          </RequesterCredentials>
          <jobId>{job_id}</jobId>
        </getJobsStatusRequest>""".format(token=self.token, job_id=job_id)

        r = requests.post(url, headers=headers, data=xml)
        nsmap = {'services': 'http://www.ebay.com/marketplace/services'}
        root = etree.fromstring(r.content)
        print r.status_code
        print r.text
        try:
            file_reference_id = root.find('services:fileReferenceId', nsmap).text
            return file_reference_id
        except AttributeError:
            return None


    def abort_job(self, job_id):
        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "abortJob",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '837',
            "X-EBAY-API-APP-NAME": "RedRocke-e380-4b45-ba54-78fb6c6832f5",
            'X-EBAY-API-DETAIL-LEVEL': '0',
            "X-EBAY-API-SITEID": '0',
            "X-EBAY-APE-CERT-NAME": "7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
            "X-EBAY-API-DEV-NAME": "f7e7239f-2cf9-4e4f-9413-1e08b524944c",
            "Content-Type": 'application/xml',
        }
        # url = "https://api.ebay.com/ws/api.dll"
        url = "https://webservices.ebay.com/BulkDataExchangeService"

        xml = """<?xml version="1.0" encoding="utf-8"?>
    <abortJobRequest xmlns="http://www.ebay.com/marketplace/services">
      <RequesterCredentials>
        <eBayAuthToken>{token}</eBayAuthToken>
      </RequesterCredentials>
      <jobId>{job_id}</jobId>
    </abortJobRequest>""".format(token=self.token, job_id=job_id)

        r = requests.post(url, headers=headers, data=xml)
        print r.status_code
        print r.text

    def get_all_created_jobs(self):
        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "getJobs",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '837',
            "X-EBAY-API-APP-NAME": "RedRocke-e380-4b45-ba54-78fb6c6832f5",
            'X-EBAY-API-DETAIL-LEVEL': '0',
            "X-EBAY-API-SITEID": '0',
            "X-EBAY-APE-CERT-NAME": "7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
            "X-EBAY-API-DEV-NAME": "f7e7239f-2cf9-4e4f-9413-1e08b524944c",
            "Content-Type": 'application/xml',
        }
        # url = "https://api.ebay.com/ws/api.dll"
        url = "https://webservices.ebay.com/BulkDataExchangeService"

        xml = """<?xml version="1.0" encoding="utf-8"?>
        <getJobsRequest xmlns="http://www.ebay.com/marketplace/services">
          <RequesterCredentials>
            <eBayAuthToken>{token}</eBayAuthToken>
          </RequesterCredentials>
          <jobType>ReviseFixedPriceItem</jobType>
        </getJobsRequest>""".format(token=self.token)

        r = requests.post(url, headers=headers, data=xml)
        print r.status_code
        print r.text

    def upload_file_request(self, job_id, file_reference_id, file_name):
        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "uploadFile",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '837',
            'X-EBAY-SOA-SERVICE-NAME': 'FileTransferService',
            'X-EBAY-SOA-REQUEST-DATA-FORMAT': 'XML',
            'X-EBAY-SOA-RESPONSE-DATA-FORMAT': 'XML',
        }
        url = "https://storage.ebay.com/FileTransferService"

        f = open(file_name, 'r')
        data = f.read()
        f.close()
        data = base64.b64encode(data)

        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <uploadFileRequest xmlns="http://www.ebay.com/marketplace/services">
          <fileAttachment>
            <Data>{data}</Data>
            <Size>{size}</Size>
          </fileAttachment>
          <fileFormat>gzip</fileFormat>
          <fileReferenceId>{file_reference_id}</fileReferenceId>
          <taskReferenceId>{job_id}</taskReferenceId>
        </uploadFileRequest>""".format(data=data, job_id=job_id, file_reference_id=file_reference_id, size=len(data))
        print xml

        r = requests.post(url, headers=headers, data=xml)
        print r.status_code
        print r.text

    def start_upload_job(self, job_id):
        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "startUploadJob",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '837',
            "X-EBAY-API-APP-NAME": "RedRocke-e380-4b45-ba54-78fb6c6832f5",
            "X-EBAY-API-CALL-NAME": 'ReviseFixedPriceItem',
            'X-EBAY-API-DETAIL-LEVEL': '0',
            "X-EBAY-API-SITEID": '0',
            "X-EBAY-APE-CERT-NAME": "7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
            "X-EBAY-API-DEV-NAME": "f7e7239f-2cf9-4e4f-9413-1e08b524944c",
            "Content-Type": 'application/xml',
        }
        # url = "https://api.ebay.com/ws/api.dll"
        url = "https://webservices.ebay.com/BulkDataExchangeService"

        xml = """<?xml version="1.0" encoding="utf-8"?>
        <startUploadJobRequest xmlns="http://www.ebay.com/marketplace/services">
          <RequesterCredentials>
            <eBayAuthToken>{token}</eBayAuthToken>
          </RequesterCredentials>
          <jobId>{job_id}</jobId>
        </startUploadJobRequest>
        """.format(job_id=job_id, token=self.token)

        r = requests.post(url, headers=headers, data=xml)
        print r.status_code
        print r.text

    def download_file(self, job_id, file_reference_id):
        headers = {
            "X-EBAY-SOA-OPERATION-NAME": "downloadFile",
            "X-EBAY-SOA-SECURITY-TOKEN": self.token,
            "X-EBAY-API-COMPATIBILITY-LEVEL": '837',
            'X-EBAY-SOA-SERVICE-NAME': 'FileTransferService',
            'X-EBAY-SOA-REQUEST-DATA-FORMAT': 'XML',
            'X-EBAY-SOA-RESPONSE-DATA-FORMAT': 'XML',
            # "X-EBAY-API-APP-NAME": "RedRocke-e380-4b45-ba54-78fb6c6832f5",
            # "X-EBAY-API-CALL-NAME": 'ReviseFixedPriceItem',
            # 'X-EBAY-API-DETAIL-LEVEL': '0',
            # "X-EBAY-API-SITEID": '0',
            # "X-EBAY-APE-CERT-NAME": "7a07bf5a-3385-4a5b-bdc9-2a66b045f0b7",
            # "X-EBAY-API-DEV-NAME": "f7e7239f-2cf9-4e4f-9413-1e08b524944c",
            # "Content-Type": 'application/xml',
        }

        url = "https://storage.ebay.com/FileTransferService"

        xml = """<?xml version="1.0" encoding="utf-8"?>
        <downloadFileRequest xmlns="http://www.ebay.com/marketplace/services">
          <fileReferenceId>{file_reference_id}</fileReferenceId>
          <taskReferenceId>{job_id}</taskReferenceId>
        </downloadFileRequest>""".format(job_id=job_id, file_reference_id=file_reference_id)

        # r = requests.post(url, headers=headers, data=xml, stream=True)
        # with open("data_dump.response", 'w') as f:
        #     r.raw.decode_content = True
        #     data = r.raw.read()
        #     f.write(data)

        r = requests.post(url, headers=headers, data=xml, stream=True)

        ebay_download_response = EbayFileDownloadResponse(StringIO(r.content))
        fname = ebay_download_response.write_file()
        return fname

    def add_item(self, data):
        """
        item_data = {
            'Item': {
                'StartPrice': '0.01',
                'ListingDuration': 'Days_1',
                'Currency': 'USD',
                'Country': 'US',
                'PrimaryCategory': {'CategoryID': '1033'},
                'Location': 'US',
                'Title': 'Ninja Gaiden',
                'Description': 'Ninja Gaiden for NES',
                'PaymentMethods': 'PayPal',
                'PayPalEmailAddress': 'paul.mouzas@gmail.com',
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
                }
            }
        }
        """

        response = self.api.execute('AddItem', data)
        return response

    def add_fixed_price_item(self, data):
        """
        data schema looks like this:
        fixed_price_data = {
            'Item': {
                'ListingDuration': 'Days_5',
                'StartPrice': '1.01',
                'Currency': 'USD',
                'Country': 'US',
                'PrimaryCategory': {'CategoryID': '1033'},
                'Location': 'US',
                'Title': 'Ninja Gaiden',
                'Description': 'Ninja Gaiden for NES',
                'PaymentMethods': 'PayPal',
                'PayPalEmailAddress': 'paul.mouzas@gmail.com',
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
                }
            }
        }
        """
        response = self.api.execute('AddFixedPriceItem', data)
        return response

    def revise_fixed_price_item(self, data):
        response = self.api.execute('ReviseFixedPriceItem', data)
        return response

    def get_my_ebay_selling(self, page_number=None):
        my_ebay_selling_request = {
            'ActiveList': {
                'Include': 'true',
                'ListingType': 'FixedPriceItem',
            }
        }

        if page_number:
            pagination = {'Pagination': {
                'PageNumber': page_number
                }
            }
            my_ebay_selling_request.update({'ActiveList': pagination})

        response = self.api.execute('GetMyeBaySelling', my_ebay_selling_request)
        return response

    def update_inventory(self, item_id, quantity):
        inventory_status = {
            'InventoryStatus': {
                'ItemID': item_id,
                'Quantity': quantity,
            }
        }
        response = self.api.execute('ReviseInventoryStatus', inventory_status)
        return response

    def update_inventory_by_sku(self, sku, quantity):
        inventory_status = {
            'InventoryStatus': {
                'SKU': sku,
                'Quantity': quantity,
            }
        }
        response = self.api.execute('ReviseInventoryStatus', inventory_status)
        return response

    def get_item_by_id(self, _id):
        get_item = {'ItemID': _id}

        response = self.api.execute('GetItem', get_item)
        return response

    def get_item_by_sku(self, sku):
        get_item = {
            'SKU': sku
        }

        response = self.api.execute('GetItem', get_item)
        return response

    def update_image_by_id(self, item_id, url):
        item = {
            'Item': {
                'ItemID': item_id,
                'PictureDetails': {
                    'PictureURL': url,
                }
            }
        }

        response = self.api.execute('ReviseFixedPriceItem', item)
        return response

    def relist_fixed_price_item(self, item_id, sku=None):
        if sku:
            item = {
                'Item': {
                    'ItemID': item_id,
                    'InventoryTrackingMethod': 'SKU',
                    'SKU': sku
                }
            }
        else:
            item = {
                'Item': {
                    'ItemID': item_id,
                }
            }

        response =  self.api.execute('RelistFixedPriceItem', item)
        return response

    def revise_tracking_method_to_sku(self, item_id, sku):
        item = {
            'Item': {
                'ItemID': item_id,
                'InventoryTrackingMethod': 'SKU',
                'SKU': sku,
            }
        }
        response = self.api.execute('RelistFixedPriceItem', item)
        return response

    def end_fixed_price_item(self, item_id):
        item = {
            'ItemID': item_id,
            'EndingReason': 'OtherListingError',
        }
        response = self.api.execute('EndFixedPriceItem', item)
        return response

    def end_item_variation(self, item_id, sku, name, value):
        item = {
            'Item': {
                'ItemID': item_id,
                'SKU': sku,
                'Variations': {
                    'Variation': {
                        'SKU': sku,
                        'VariationSpecifics': {
                            'NameValueList': {
                                'Name': name,
                                'Value': value,
                            }
                        }
                    },
                }
            }
        }
        print item
        response = self.api.execute('EndFixedPriceItem', item)
        return response

    def update_item_variation(self, item_id, quantity, name, value):

        item = {
            'Item': {
                'ItemID': item_id,
                'Variations': {
                    'Variation': {
                        'Quantity': quantity,
                        'VariationSpecifics': {
                            'NameValueList': {
                                'Name': name,
                                'Value': value,
                            }
                        }
                    },
                }
            }
        }
        response = self.api.execute('ReviseFixedPriceItem', item)
        return response

    def add_upc_code_to_item(self, item_id, upc):
        item = {
            'Item': {
                'ItemID': item_id,
                'ProductListingDetails': upc,
            }
        }
        response = self.api.execute('ReviseFixedPriceItem', item)
        return response

    def add_upc_code_to_item_variation(self, item_id, upc, name, value):
        item = {
            'Item': {
                'ItemID': item_id,
                'Variations': {
                    'Variation': {
                        'VariationProductListingDetails': {
                            'UPC': upc,
                        },
                        'VariationSpecifics': {
                            'NameValueList': {
                                'Name': name,
                                'Value': value,
                            }
                        }
                    },
                }
            }
        }
        response = self.api.execute('ReviseFixedPriceItem', item)
        return response

    def bulk_add_upc(self, items):
        request_data = []
        for item in items:
            item_id, upc, name, value = item
            element = {
                'Item': {
                    'ItemID': item_id,
                    'Variations': {
                        'Variation': {
                            'VariationProductListingDetails': {
                                'UPC': upc,
                            },
                            'VariationSpecifics': {
                                'NameValueList': {
                                    'Name': name,
                                    'Value': value,
                                }
                            }
                        },
                    }
                }
            }
            request_data.append(element)
        response = self.api.execute('ReviseFixedPriceItem', request_data)
        return response

    def update_item_variation_quantity_by_item_id_and_sku(self, item_id, sku, quantity):
        item = {
            'Item': {
                'ItemID': item_id,
                'Variations': {
                    'Variation': {
                        'SKU': sku,
                        'Quantity': quantity,
                    },
                }
            }
        }
        response = self.api.execute('ReviseFixedPriceItem', item)
        return response

    def update_item_variation2(self, item_id, varsku):
        item = {'ItemID': item_id, 'VariationSKU': varsku}
        response = self.api.execute('ReviseFixedPriceItem', item)
        return response

    def end_item(self, item_id):
        end = {
            'EndingReason': 'NotAvailable',
            'ItemID': item_id
        }
        response = self.api.execute('EndItem', end)
        return response

    def get_all_active_orders(self, days=30):
        get_orders_request = {
            'OrderStatus': 'Active',
            'NumberOfDays': days,
        }
        response = self.api.execute('GetOrders', get_orders_request)

        return response

    def get_all_completed_orders(self, page=1, days=30):
        get_orders_request = {
            'OrderStatus': 'Completed',
            'Pagination': {
                'PageNumber': page,
            },
            'NumberOfDays': days,
        }
        response = self.api.execute('GetOrders', get_orders_request)

        return response

    def get_orders(self, status, page=1, days=30):
        get_orders_request = {
            'OrderStatus': status,
            'Pagination': {
                'PageNumber': page,
            },
            'NumberOfDays': days,
        }
        response = self.api.execute('GetOrders', get_orders_request)
        return response

    def complete_sale(self, tracking_code, carrier, transaction_id, item_id):
        # complete_sale_request = {
        #     'OrderLineItemId': order_line_item_id,
        #     'ShipmentTrackingDetails': {
        #         'ShipmentTrackingNumber': tracking_code,
        #         'ShippingCarrierUsed': carrier
        #     },
        #     'Shipped': 'true',
        #     'TransactionID': transaction_id
        # }
        complete_sale_request = {
            'Shipment': {
                'ShipmentTrackingDetails': {
                    'ShipmentTrackingNumber': tracking_code,
                    'ShippingCarrierUsed': carrier
                }
            },
            'Shipped': 'true',
            'TransactionID': transaction_id,
            'ItemID': item_id
        }

        response = self.api.execute('CompleteSale', complete_sale_request)
        return response

    def complete_sale_by_sku(self, tracking_code, carrier, transaction_id, sku):
        # complete_sale_request = {
        #     'OrderLineItemId': order_line_item_id,
        #     'ShipmentTrackingDetails': {
        #         'ShipmentTrackingNumber': tracking_code,
        #         'ShippingCarrierUsed': carrier
        #     },
        #     'Shipped': 'true',
        #     'TransactionID': transaction_id
        # }
        complete_sale_request = {
            'Shipment': {
                'ShipmentTrackingDetails': {
                    'ShipmentTrackingNumber': tracking_code,
                    'ShippingCarrierUsed': carrier
                }
            },
            'Shipped': 'true',
            'TransactionID': transaction_id,
            'SKU': sku
        }

        response = self.api.execute('CompleteSale', complete_sale_request)
        return response

    # def complete_multiple_sale(self, order_id,):
    #
    #     complete_sale_request = {
    #         'ShipmentTrackingDetails': {
    #             'ShipmentTrackingNumber': tracking_code,
    #             'ShippingCarrierUsed': carrier
    #         },
    #         'Shipped': 'true',
    #         'TransactionID': transaction_id,
    #         'ItemID': item_id
    #     }
    #
    #     response = self.api.execute('CompleteSale', complete_sale_request)
    #     return response


    def get_order_by_order_id(self, order_id):
        get_orders_request = {
            'OrderIDArray': [
                {'OrderID': order_id}
            ]
        }
        response = self.api.execute('GetOrders', get_orders_request)
        return response
