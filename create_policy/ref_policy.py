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
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra', required=False)
    args = parser.parse_args(argv)

    with open('../default_config/products/personal-auto/policy/exposures/vehicle/perils/' +
              'bodily_injury.premium.liquid', "r") as f:
        calculation = f.read()

    print 'Authenticating with tenant: ' + args.hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password)

    ph_values = {
        'first_name': ['Gary'],
        'last_name': ['Richards']
    }

    ph = client.create_policyholder(values=ph_values)
    ph_locator = ph['locator']

    with open('ref_exposure.json', 'r') as f:
        exp_values = json.load(f)
    with open('ref_policy.json', 'r') as f:
        policy_values = json.load(f)
    with open('ref_driver.json', 'r') as f:
        driver = json.load(f)

    peril = {'name': 'bodily_injury'}
    exposure = {'exposureName': 'vehicle',
                'fieldValues': exp_values['required'],
                'perils': [peril]
                }

    start_timestamp = dates.date_to_millis(
        '30/11/2017', 'America/Los_Angeles', "%d/%m/%Y")
    end_timestamp = dates.date_to_millis(
        '30/11/2018', 'America/Los_Angeles', "%d/%m/%Y")
    policy = client.create_policy('personal-auto', ph_locator,
                                  policy_start_timestamp=start_timestamp,
                                  policy_end_timestamp=end_timestamp,
                                  field_values=policy_values['required'],
                                  field_groups=[driver, driver],
                                  exposures=[exposure, exposure],
                                  finalize=False)

    print json.dumps(policy)
    policy_locator = policy['locator']
    client.uw_policy(policy_locator)
    client.price_policy(policy_locator)
    client.finalize_policy(policy_locator)

    # print json.dumps(policy)
    peril_id = policy['exposures'][0]['perils'][0]['displayId']
    print 'Policy Locator: ' + policy_locator
    print '-----'
    uw_result = client.uw_policy(policy_locator)
    print json.dumps(uw_result)
    print '----'
    price_result = client.price_policy(policy_locator)
    print json.dumps(price_result)
    print '----'
    detailed_price_result = client.check_existing_peril_premium(
        calculation, peril_id)
    print json.dumps(detailed_price_result,
                     sort_keys=True, indent=4, separators=(',', ':')) + "\n"


if __name__ == "__main__":
    main(sys.argv[1:])
