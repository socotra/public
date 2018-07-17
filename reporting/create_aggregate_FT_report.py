import argparse
import requests
import sys
import time
from socotratools.client import SocotraClient
from socotratools import dates
import csv
from itertools import groupby
from operator import itemgetter

# ETL application to aggregate financial transaction
# report by lines of business.

# Usage:
# python create_aggregate_FT_report.py
#       -n <hostname>
#       -u <username>
#       -n <password>
#       -s <report start date>, e.g., 2018-7-01
#       -e <report end date>, e.g., 2018-07-31
#       -o <outputfile>, e.g., outfile


def parse_args():
    parser = argparse.ArgumentParser(
        description='Main Test Application')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra', required=False)
    parser.add_argument('-s', '--startdate', required=True)
    parser.add_argument('-e', '--enddate', required=True)
    parser.add_argument('-o', '--outputfile', required=True)

    return parser.parse_args()


def get_report_timestamps(startdate, enddate):
    start_timestamp = dates.date_to_millis(startdate, 'Europe/Berlin', "%Y-%m-%d")
    end_timestamp = dates.date_to_millis(enddate, 'Europe/Berlin', "%Y-%m-%d")
    return start_timestamp, end_timestamp

def get_ft_report(args, client):
    # convert start and end dates to timestamps
    start_ts, end_ts = get_report_timestamps(args.startdate, args.enddate)

    # start running the uep report
    report_name = 'financialTransaction'
    report_locator = client.generate_report(report_name, start_ts, end_ts)['locator']

    # retrieve report status
    report_status = client.get_report(report_locator)['status']

    # check that report has not failed every 5 seconds
    while report_status != 'failed' and report_status == 'started':
        time.sleep(5)
        report_status = client.get_report(report_locator)['status']

    # get the report url
    report_url = client.get_report(report_locator)['resultUrl']

    # retrieve the report text
    report = requests.get(report_url).text

    return report


def get_aggregate_report(report):
    # convert report into a dictionary 
    reader = csv.DictReader(report.splitlines())
    ft_dict = []
    for line in reader:
        ft_dict.append(line)

    # define the filter key
    grouper = itemgetter("Product Name", "Transaction Type")

    result = []
    for key, grp in groupby(sorted(ft_dict, key=grouper), grouper):
        temp_dict = dict(zip(["Product Name", "Transaction Type"], key))
        temp_dict["Amount"] = round(sum(float(item["Amount"]) for item in grp), 2)
        result.append(temp_dict)

    return result


def write_output(outputfile, aggr_dict):
    keys = aggr_dict[0].keys()
    with open(outputfile, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(aggr_dict)
        print("writing complete")


def main(argv):

    args = parse_args()

    print 'Authenticating with tenant: ' + args.hostname

    # create a client
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password)

    # retrieve the report text
    report = get_ft_report(args, client)

    # aggregate the report (this is a dictionary)
    aggr_report = get_aggregate_report(report)

    # write aggregate report to file
    write_output(args.outputfile, aggr_report)


if __name__ == "__main__":
    main(sys.argv[1:])
