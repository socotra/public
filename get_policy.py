import argparse
import json
import sys
from socotratools.client import SocotraClient

# Helper application to see the raw values of a given policy locator from a
# specifeid tenant.


def main(argv):

    parser = argparse.ArgumentParser(
        description='Get Policy')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='iag.tester', required=False)
    parser.add_argument('-p', '--password', default='Satellit31!', required=False)
    parser.add_argument('-l', '--locator', required=True)
    args = parser.parse_args(argv)

    print 'Authenticating with tenant: ' + args.hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password,
        api_url='https://api-iag.socotra.com')

    policy = client.get_policy(args.locator)
    print json.dumps(policy)


if __name__ == "__main__":
    main(sys.argv[1:])
