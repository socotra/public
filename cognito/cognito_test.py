import argparse
import json
import sys
import cognito_provider
from socotratools.client import SocotraClient


# Test file to generate a policyholder if allowed by the provided
# cognito directory service.

#  python cognito_test.py -n <hostname> -u <cognito_user> -p <cognito_password>


def main(argv):

    parser = argparse.ArgumentParser(
        description='Main Test Application')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-p', '--password', required=True)
    parser.add_argument('-i', '--identity', required=False)
    args = parser.parse_args(argv)

    if args.identity:
        provider = cognito_provider.CognitoIdentity(args.identity)
    else:
        provider = None

    print 'Authenticating with tenant: ' + args.hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password, debug=False, identity=provider)

    # setup for super simple policyholder configuration
    ph_values = {
        'first_name': ['Gary'],
        'last_name': ['Richards']
    }

    ph = client.create_policyholder(values=ph_values)
    print ph['locator']


if __name__ == "__main__":
    main(sys.argv[1:])
