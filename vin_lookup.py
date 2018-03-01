import sys
import json
import requests
import argparse


def process_vin(vin_input):
    return_value = {}

    # Make request call to NHTSA database
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    post_fields = {'format': 'json', 'data': vin_input}
    r = requests.post(url, data=post_fields)
    vin_return = json.loads(r.text)

    # Check if there was a successful result
    if vin_return.get('Count') == 1:
        print 'Success'
        car = vin_return['Results'][0]
        make = car['Make']
        model = car['Model']
        model_year = car['ModelYear']

        return_value['fieldValues'] = {'make': make,
                                       'model': model,
                                       'model_year': model_year
                                       }

    return return_value


def lambda_handler(event, context):

    vin = event['policy']['characteristics'][0]['fieldValues']['vin']
    return process_vin(vin)


def main(argv):
    # Used for testing the process_vin() function.

    parser = argparse.ArgumentParser(
        description='VIN Lookup Application')
    # samples:  3GNDA13D76S000000;2HGEJ6526VH515413
    parser.add_argument('-v', '--vin', required=True)
    args = parser.parse_args(argv)

    result = process_vin(args.vin)
    print json.dumps(result)


if __name__ == "__main__":
    main(sys.argv[1:])
