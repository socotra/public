import argparse
import json
import csv
import sys
from socotratools.client import SocotraClient


def process_row(writer, row, accounts):
    txn_type = row['Transaction Type']

    if txn_type == 'premium':
        gen_gl_txn(writer, row, 1, accounts[txn_type]['debit'])
        gen_gl_txn(writer, row, 2, accounts[txn_type]['credit'], -1)
    elif txn_type == 'fee':
        gen_gl_txn(writer, row, 1, accounts[txn_type]['debit'])
        gen_gl_txn(writer, row, 2, accounts[txn_type]['credit'], -1)
    elif txn_type == 'commission':
        gen_gl_txn(writer, row, 1, accounts[txn_type]['debit'])
        gen_gl_txn(writer, row, 2, accounts[txn_type]['credit'], -1)


def gen_gl_txn(writer, row, line_no, account_no, direction_factor=1):

    txn_row = {}
    txn_row['Business Unit'] = 'Marketing'
    txn_row['Book Code'] = '45'
    txn_row['Rate Type'] = 'CRRNT'

    # Extract relevant information from source
    date = row['Payment Posted Date']
    desc = row['Product Name'] + ': ' + \
        row['Fee Name'] + ': ' + \
        row['Transaction Type']

    txn_row['Journal ID'] = 'ACME' + date
    txn_row['Journal Date'] = date
    txn_row['Header Description'] = desc
    txn_row['Line'] = line_no
    txn_row['Account'] = account_no
    txn_row['Journal Line Reference'] = row['Policy ID']
    txn_row['Currency'] = row['Currency']
    txn_row['Amount'] = float(row['Amount']) * direction_factor

    if float(row['Amount']) != 0:
        writer.writerow(txn_row)


def main(argv):

    parser = argparse.ArgumentParser(
        description='Main Test Application')
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='output.csv',
                        required=False)

    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra', required=False)
    args = parser.parse_args(argv)

    # print 'Authenticating with tenant: ' + args.hostname
    # client = SocotraClient.get_authenticated_client_for_hostname(
    #     args.hostname, args.username, args.password)

    output_file = open(args.output, 'w')
    headers = json.load(open('headers.json'))
    writer = csv.DictWriter(output_file, fieldnames=headers)
    writer.writeheader()

    report_file = open(args.input, 'r')
    report_reader = csv.DictReader(report_file)

    accounts = json.load(open('accounts.json'))

    for row in report_reader:
        process_row(writer, row, accounts)


if __name__ == "__main__":
    main(sys.argv[1:])
