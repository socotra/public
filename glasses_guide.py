from suds.client import Client
import sys
import argparse
import json
from suds.xsd.doctor import Import, ImportDoctor
from suds.sax.element import Element
from suds.sax.attribute import Attribute

# This script can be used to lookup vehicle details from Glasses Guide.
# by passing in an NVIC identifier and retrieving details like vehicle
# make, model, year, and value.


def get_gg_details(nvic, username, password):

    url = "http://eurotaxglasswebservices.com.au/GeneralGGWebService.asmx?WSDL"

    imp = Import('http://www.w3.org/2001/XMLSchema',
                 location='http://www.w3.org/2001/XMLSchema.xsd')
    imp.filter.add('http://microsoft.com/webservices/')

    client = Client(url, doctor=ImportDoctor(imp))

    code = Element('Username').setText(username)
    pwd = Element('Password').setText(password)

    reqsoapheader = Element('AuthHeader').insert(code)
    reqsoapheader = reqsoapheader.append(pwd)
    reqsoap_attribute = Attribute('xmlns', "http://microsoft.com/webservices/")
    reqsoapheader.append(reqsoap_attribute)
    client.set_options(soapheaders=reqsoapheader)
    # print client   # shows the details of this service

    result = client.service.GetDetailsSpecificationAll('A', nvic)
    details = result.diffgram.NewDataSet.DataSepcDetails
    # print details
    return details


def lookup_value(nvic):

    details = get_gg_details(nvic, '<gg_username>', '<gg_password>')

    make = details.ManufacturerName
    model = details.FamilyName
    variant = details.VariantName
    year = details.YearCreate
    value = details.Trade

    return {'fieldValues': {'vehicle_make': [make],
                            'vehicle_model': [model],
                            'vehicle_varient': [variant],
                            'vehicle_year': [year],
                            'gg_value': [value],
                            }
            }


def lambda_handler(event, context):

    print event
    reg_num = event['body-json'][
        'exposureCharacteristics']['fieldValues']['nvic'][0]

    return lookup_value(reg_num)


def main(argv):
    parser = argparse.ArgumentParser(
        description='Lookup NVIC Details Test Application')
    # Sample NVIC:  "123"
    parser.add_argument('-n', '--nvic', required=True)
    args = parser.parse_args(argv)

    value = lookup_value(args.nvic)
    print json.dumps(value)


if __name__ == '__main__':
    main(sys.argv[1:])
