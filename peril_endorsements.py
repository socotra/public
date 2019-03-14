#!/usr/bin/env python
import json
import urlparse

import requests


def peril_endorsement():
    print('Getting auth token.')

    api_url = 'https://api.develop.socotra.com/account/authenticate'
    local_api_url = 'http://127.0.0.1:8080/account/authenticate'
    host_name = 'vishnu-configeditor.co.develop.socotra.com'
    local_host_name = 'vishnu-vishnu1.co.develop.socotra.com'
    base_policy_url = 'https://api.develop.socotra.com/policy'
    policy_id = '100005500'

    payload = {
        'username': 'alice.lee',
        'password': 'socotra',
        'hostName': host_name
    }

    auth_response = requests.post(api_url, json=payload)
    auth_token = auth_response.json()['authorizationToken']
    print('Retrieved the auth token.')

    policy_url = base_policy_url + '/' + policy_id
    headers = {
        'content-type': 'application/json',
        'Authorization': auth_token
    }

    policy_response = requests.get(policy_url, headers=headers)
    exposure = policy_response.json()['exposures'][0]
    exposure_locator = exposure['locator'].encode('ascii', 'ignore')
    perils = exposure['perils']

    peril_locator_to_remove = perils[1]['locator'].encode('ascii', 'ignore')
    peril_locator_to_update = perils[2]['locator'].encode('ascii', 'ignore')

    # deductible = "100"
    # lumpSumPayment = "200"
    # perilUpdateRequest = {
    #     'addFieldGroups': [],
    #     'fieldValues': {},
    #     'perilLocator': peril_locator_to_update,
    #     'removeFieldGroup': [],
    #     'updateFieldGroups': [],
    #     'deductible': deductible,
    #     'lumpSumPayment': lumpSumPayment,
    #     'removeIndemnityPerEvent': False,
    #     'removeIndemnityPerItem': False
    # }
    #
    # exposure_update_request = {
    #     'addFieldGroups': [],
    #     'addPerils': [],
    #     'endPerils': [],
    #     'exposureLocator': exposure_locator,
    #     'fieldValues': {},
    #     'removeFieldGroups': [],
    #     'updateFieldGroups': [],
    #     'updatePerils': [perilUpdateRequest]
    # }

    # exposure_update_request = {
    #     'addFieldGroups': [],
    #     'addPerils': [],
    #     'endPerils': [peril_locator_to_remove],
    #     'exposureLocator': exposure_locator,
    #     'fieldValues': {},
    #     'removeFieldGroups': [],
    #     'updateFieldGroups': [],
    #     'updatePerils': []
    # }

    exposure_update_request = {
        'addFieldGroups': [],
        'addPerils': [{"name":"bodily_injury"}],
        'endPerils': [],
        'exposureLocator': exposure_locator,
        'fieldValues': {},
        'removeFieldGroups': [],
        'updateFieldGroups': [],
        'updatePerils': []
    }

    policy_update_request = {
        'addExposures': [],
        'addFieldGroups': [],
        'endExposures': [],
        'fieldValues': {},
        'removeFieldGroups': [],
        'updateExposures': [exposure_update_request],
        'updateFieldGroups': [],
        'hasPolicyUpdates': False
    }

    endorsement_request = {
        'endorsementName': 'generic',
        'startTimestamp': 1565852400000,
        'updatePolicy': policy_update_request
    }

    endorsement_url = base_policy_url + '/' + policy_id + '/endorse'
    endorsement_response = requests.post(endorsement_url, json=endorsement_request, headers=headers)

    updated_policy = requests.get(policy_url, headers=headers)
    updated_policy_data = updated_policy.json()
    print(updated_policy_data)

    if __name__ == '__main__':
        peril_endorsement()
