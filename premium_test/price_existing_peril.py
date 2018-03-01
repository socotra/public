import argparse
import json
from socotratools.client import SocotraClient

# python scripts/price_existing_peril.py -i 100000309
# -c basic.calculation.liquid
# -n starterkit-testuser.co.sandbox.socotra.com -u alice.lee -p socotra

parser = argparse.ArgumentParser(
    description="Check the premium of an existing peril")

parser.add_argument("-i", "--peril_id", help="Id of peril to price")
parser.add_argument("-c", "--calculation_file", help="liquid file")

parser.add_argument("-n", "--hostname")
parser.add_argument("-u", "--username", default="alice.lee")
parser.add_argument("-p", "--password", default="socotra")
args = parser.parse_args()

socotra_client = SocotraClient.get_authenticated_client_for_hostname(
    args.hostname,
    args.username,
    args.password,
    debug=False)

with open(args.calculation_file, "r") as f:
    calculation = f.read()

response = socotra_client.check_existing_peril_premium(
    calculation, args.peril_id)
print json.dumps(response, sort_keys=True, indent=4, separators=(',', ':')) + "\n"
