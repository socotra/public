#!/usr/bin/env python
import argparse
import sys
import json
from socotratools.client import SocotraClient
import myrater


# The external rater only gives us characteristic locators and the policy,
# but we actually want the full characteristic and the full exposure and
# peril from the policy to do the appropriate calculations.  This method
# returns the characteristic object and parent object for use in process_.

def get_relevant_objs(policy, triplet):
    data = {}

    # convert from triplet chars to triplet char_locators
    for policy_char in policy['characteristics']:
        if policy_char['locator'] == triplet['policyCharacteristicsLocator']:
            data['current_policy_char'] = policy_char

    for exposure in policy['exposures']:
        for exp_char in exposure['characteristics']:
            if exp_char['locator'] == triplet['exposureCharacteristicsLocator']:
                data['current_exp_char'] = exp_char
                data['current_exposure'] = exposure

        for peril in exposure['perils']:
            for peril_char in peril['characteristics']:
                if peril_char['locator'] == triplet['perilCharacteristicsLocator']:
                    data['current_peril_char'] = peril_char
                    data['current_peril'] = peril
    return data


# Main worker method which processes each set of characteristic locators
# (the "triplet") and returns the premium in the corresponding structure
# for the external rater,

def process_triplets(policy, triplets):
    return_value = {}
    return_value['pricedPerilCharacteristics'] = {}
    price_return_value = return_value['pricedPerilCharacteristics']

    for triplet in triplets:
        data = get_relevant_objs(policy, triplet)
        premium = myrater.price_peril(data)

        # Socotra requires the return value to be in this format.
        price_return_value[
            triplet['perilCharacteristicsLocator']] = {'premium': premium}

    return return_value


# This method is the entry point for the AWS lambda process which receives the
# external data call request from Socotra.  See README for more details.

def lambda_handler(event, context):
    print json.dumps(event)
    policy = event['body-json']['policy']
    triplets = event['body-json']['policyExposurePerils']

    output = process_triplets(policy, triplets)
    print json.dumps(output)    # Provided for logging purposes
    return output


# Test method to validate the logic for the external rater without using
# the Socotra UI.  Requires the policy ID as an input to be priced.

# This test method tests all the perils for the first exposure and first
# set of characteristics

def main(argv):
    parser = argparse.ArgumentParser(
        description='Main Test Application')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra',
                        required=False)
    parser.add_argument('-i', '--id', required=True)

    args = parser.parse_args(argv)
    hostname = args.hostname
    print 'Authenticating with tenant: ' + hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        hostname, args.username, args.password)
    policy = client.get_policy(args.id)

    # assumes at least one set of characteristics exists on the policy.
    # Only prices the first exposure.
    policy_char_locator = policy['characteristics'][0]['locator']
    exp_char_locator = policy['exposures'][0]['characteristics'][0]['locator']

    # Create a set of triplets which mocks the payload that will be generated
    # by the payload in the external rater.  A triplet is a set of characteristic
    # locators that will be passed into the rater.

    triplets = []
    for peril in policy['exposures'][0]['perils']:
        peril_char_locator = peril['characteristics'][0]['locator']

        triplets.append({'policyCharacteristicsLocator': policy_char_locator,
                         'exposureCharacteristicsLocator': exp_char_locator,
                         'perilCharacteristicsLocator': peril_char_locator})

    output = process_triplets(policy, triplets)
    print json.dumps(output)


if __name__ == "__main__":
    main(sys.argv[1:])
