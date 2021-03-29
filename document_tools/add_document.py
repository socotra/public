import argparse
import json
import os

from socotratools.client import SocotraClient

# python add_document.py -pl <locator>
# -d test.html -n <username>-configeditor.co.sandbox.socotra.com

parser = argparse.ArgumentParser(description="Add a document to a policy")
parser.add_argument("-pl", "--policy_locator", required=True)
parser.add_argument("-d", "--document", help="Path to document (PDF or HTML)",
                    required=True)
parser.add_argument("-dn", "--display_name",
                    help="Display name for document (defaults to file name)")

parser.add_argument("-n", "--hostname", required=True)
parser.add_argument("-u", "--username", default="alice.lee", help="Username")
parser.add_argument("-p", "--password", default="socotra", help="Password")
args = parser.parse_args()

client = SocotraClient.get_authenticated_client_for_hostname(
    args.hostname, args.username, args.password, debug=False)

document_type = os.path.splitext(args.document)[1][1:]
if document_type not in ['pdf', 'html']:
    raise Exception("Document must be a pdf or html file")

with open(args.document) as document:
    display_name = args.display_name if args.display_name else os.path.basename(
        document.name)
    response = client.add_document_to_policy(
        args.policy_locator, display_name, document_type, document)
    print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
