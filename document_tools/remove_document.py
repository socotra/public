import argparse
import json
from socotratools.client import SocotraClient

# python remove_document.py
# -pl <policy locator>
# -dl <document locator>
# -n <username>-configeditor.co.sandbox.socotra.com

parser = argparse.ArgumentParser(description="Remove a document from a policy")
parser.add_argument("-pl", "--policy_locator", required=True)
parser.add_argument("-dl", "--document_locator", required=True)

parser.add_argument("-n", "--hostname", help="Tenant host name", required=True)
parser.add_argument("-u", "--username", default="alice.lee", help="Username")
parser.add_argument("-p", "--password", default="socotra", help="Password")
args = parser.parse_args()

client = SocotraClient.get_authenticated_client_for_hostname(
    args.hostname, args.username, args.password, debug=False)

response = client.remove_document_from_policy(args.policy_locator,
                                              args.document_locator)
print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
