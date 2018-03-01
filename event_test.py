import argparse
import json
import sys
from socotratools.client import SocotraClient
from socotratools import dates


def process_events(events):
    for event in events:
        print event['id'] + ' - ' + event['type'] + ' - ' + event['timestamp']


def main(argv):

    parser = argparse.ArgumentParser(
        description='Main Test Application')
    # times should be in YYYY-MM-dd format
    parser.add_argument('-s', '--start', required=True)
    parser.add_argument('-f', '--finish', required=True)

    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra', required=False)
    args = parser.parse_args(argv)

    print 'Authenticating with tenant: ' + args.hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password)

    start = dates.date_to_millis(args.start,
                                 'America/Los_Angeles', '%Y-%m-%d')
    finish = dates.date_to_millis(args.finish,
                                  'America/Los_Angeles', '%Y-%m-%d')

    token = None
    while True:
        response = client.get_events(start_timestamp=start,
                                     end_timestamp=finish,
                                     paging_token=token)
        process_events(response['events'])
        if 'pagingToken' not in response.keys():
            break
        token = response['pagingToken']


if __name__ == "__main__":
    main(sys.argv[1:])
