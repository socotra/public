import argparse
import json
import sys
from socotratools.client import SocotraClient
from socotratools import dates


# Helper to generate a policy with input from the current folder
# and look at the UW decision and final premium to validate
# new functionality


def main(argv):

    parser = argparse.ArgumentParser(
        description='Main Test Application')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-l', '--locator', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password',
                        default='socotra', required=False)
    parser.add_argument('--environment', '-e',
                        help='Environment',
                        choices=['sandbox', 'iag', 'perf'], default='sandbox',
                        required=False)

    args = parser.parse_args(argv)

    policy_locator = args.locator

    with open('ref_driver.json', 'r') as f:
        driver = json.load(f)

    print 'Authenticating with tenant: ' + args.hostname
    environment = args.environment
    if environment == 'iag':
        url = 'https://api-iag.socotra.com'
    elif environment == 'perf':
        url = 'https://api-db-internal.socotra.com'
    else:
        url = 'https://api.sandbox.socotra.com'
    print url
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password, api_url=url, debug=False)

    en1_eff = dates.date_to_millis(
        '01/04/2020', 'America/Los_Angeles', '%d/%m/%Y')
    policy_change = {"channel": "Agent"}
    en1 = client.create_endorsement(
        policy_locator, 'generic', effective_timestamp=en1_eff,
        field_values=policy_change)
    print json.dumps(en1)
    en1_locator = en1['locator']
    print en1_locator

    en1_price = client.price_endorsement(en1_locator)
    print json.dumps(en1_price)
    print
    en1 = client.get_endorsement(en1_locator)
    print json.dumps(en1)

    accept_result = client.update_endorsement(en1_locator, action='accept')
    print json.dumps(accept_result)
    print
    en1 = client.get_endorsement(en1_locator)
    print json.dumps(en1)
    print en1['documents'][0]['url']


if __name__ == "__main__":
    main(sys.argv[1:])
