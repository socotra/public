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
    parser.add_argument('-p', '--password', default='socotra', required=False)
    args = parser.parse_args(argv)

    policy_locator = args.locator

    print 'Authenticating with tenant: ' + args.hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password)

    rn1_end = dates.date_to_millis(
        '30/10/2019', 'Australia/Sydney', "%d/%m/%Y")
    rn1 = client.create_renewal(policy_locator, end_timestamp=rn1_end)
    print rn1
    rn1_locator = rn1['locator']
    rn1 = client.update_renewal(rn1_locator, action='accept')
    rn1 = client.update_renewal(rn1_locator, action='invalidate')
    rn2 = client.create_renewal(policy_locator, end_timestamp=rn1_end)
    rn2_locator = rn2['locator']
    rn2 = client.update_renewal(rn2_locator, action='accept')
    print rn1
    print rn2


if __name__ == "__main__":
    main(sys.argv[1:])
