import argparse
import json

from socotratools.client import SocotraClient

# Render a policy document:
# python render_document.py -i 100000301 -d ./template.liquid
#   -n <username>-configeditor.co.sandbox.socotra.com

parser = argparse.ArgumentParser(description="Render a document for a policy")
parser.add_argument("-i", "--policy_id", help="policy id", required=True)
parser.add_argument("-d", "--document_template_file",
                    help="liquid document template file", required=True)

parser.add_argument("-n", "--hostname", help="Tenant host name", required=True)
parser.add_argument("-u", "--username", default="alice.lee", help="Username")
parser.add_argument("-p", "--password", default="socotra", help="Password")
args = parser.parse_args()

client = SocotraClient.get_authenticated_client_for_hostname(
    args.hostname, args.username, args.password, debug=False)

with open(args.document_template_file, "r") as f:
    template = f.read()

response = client.render_policy_document(args.policy_id, template)

print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ':')) + "\n")
