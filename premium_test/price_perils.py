import argparse
import json
import sys
from socotratools.client import SocotraClient


# Check the premium based on a single json file
# describing the peril.
#
# python price_perils.py -pr auto
# -c basic.calculation.liquid -r test_peril.json
# -n <username>-configeditor.co.sandbox.socotra.com


def main(argv):
    parser = argparse.ArgumentParser(
        description="Get premiums for a set of perils in JSON")
    parser.add_argument("-c", "--calculation_file", help="Liquid calculation ")
    parser.add_argument("-r", "--peril_request", help="JSON with peril info")
    parser.add_argument("-pr", "--product", help="Product Name", required=True)

    parser.add_argument("-n", "--hostname", help="Tenant host name")
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

    with open(args.peril_request, "r") as f:
        request_json = json.loads(f.read())
    response = socotra_client.check_peril_premium(
        args.product,
        calculation,
        request_json["policyCharacteristics"],
        request_json["exposureName"],
        request_json["exposureCharacteristics"],
        request_json["perilName"],
        request_json["perilCharacteristics"])
    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ':')) + "\n"


if __name__ == "__main__":
    main(sys.argv[1:])
