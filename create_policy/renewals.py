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
        '30/10/2020', 'Australia/Sydney', "%d/%m/%Y")
    policy_change = {"channel": "Agent"}
    rn1 = client.create_renewal(
        policy_locator, field_values=policy_change, end_timestamp=rn1_end)
    rn1_locator = rn1['locator']
    print rn1_locator
    # print json.dumps(rn1)

    # rn1_price = client.price_renewal(rn1_locator)
    # print json.dumps(rn1_price)
    # print
    # rn1 = client.get_renewal(rn1_locator)
    # print json.dumps(rn1)

    accept_result = client.update_renewal(rn1_locator, action='issue')
    print json.dumps(accept_result)
    # print
    # rn1 = client.get_renewal(rn1_locator)
    # print json.dumps(rn1)

    # rn1 = client.update_renewal(rn1_locator, action='invalidate')

    # rn2 = client.create_renewal(policy_locator, end_timestamp=rn1_end)
    # rn2_locator = rn2['locator']
    # rn2 = client.update_renewal(rn2_locator, action='accept')
    # print rn1
    # print rn2

    # print
    # renewals = client.get_renewals_from_policy(policy_locator)
    # print json.dumps(renewals)
    # print
    # policy = client.get_policy(policy_locator)
    # print json.dumps(policy)


if __name__ == "__main__":
    main(sys.argv[1:])
