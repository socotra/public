import argparse
import json
import csv
import os
import sys
# from socotratools.client import SocotraClient


def write_fields(writer, fields, product, exposure='-', peril='-'):

    for field in fields:
        # possibly add a required/optional column?
        # should we deal with conditinoals?

        field_row = {}
        field_row['product'] = product
        field_row['exposure'] = exposure
        field_row['peril'] = peril
        field_row['field_name'] = field['name']
        field_row['type'] = field['type']
        writer.writerow(field_row)

        # Add subfields
        for subfield in field.get('fields', []):
            field_row = {}
            field_row['product'] = product
            field_row['exposure'] = exposure
            field_row['peril'] = peril
            field_row['field_name'] = field['name'] + "\\" + subfield['name']
            field_row['type'] = subfield['type']
            writer.writerow(field_row)

# Example:  gen_data_dictionary.py -d ~/socotra_config
def main(argv):

    parser = argparse.ArgumentParser(
        description='Data Dictionary Generator')
    parser.add_argument('-o', '--output', default='output.csv',
                        required=False)
    parser.add_argument('-d', '--directory', help='Config folder')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra', required=False)
    args = parser.parse_args(argv)

    # print 'Authenticating with tenant: ' + args.hostname
    # client = SocotraClient.get_authenticated_client_for_hostname(
    #     args.hostname, args.username, args.password)

    base_dir = args.directory
    output_file = open(args.output, 'w')
    headers = [
        "product",
        "exposure",
        "peril",
        "field_name",
        "type"
    ]

    writer = csv.DictWriter(output_file, fieldnames=headers)
    writer.writeheader()

    product_dir = base_dir + '/products'
    for product in sorted(os.listdir(product_dir)):
        if product.startswith('.'):
            continue
        policy = json.load(open(product_dir + '/' + product +
                                '/policy/policy.json'))
        write_fields(writer, policy['fields'], product)
        exp_dir = product_dir + '/' + product + '/policy/exposures'
        for exp in sorted(os.listdir(exp_dir)):
            if exp.startswith('.'):
                continue
            exposure = json.load(open(exp_dir + '/' + exp + '/exposure.json'))
            write_fields(writer, exposure['fields'], product, exp)
            peril_dir = exp_dir + '/' + exp + '/perils'
            for peril in sorted(os.listdir(peril_dir)):
                if peril.startswith('.') or peril.endswith('.liquid'):
                    continue
                peril = json.load(open(peril_dir + '/' + peril))
                write_fields(writer, peril['fields'], product, exp, peril)


if __name__ == "__main__":
    main(sys.argv[1:])
