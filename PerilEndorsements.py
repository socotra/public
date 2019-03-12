import requests
import json

def perilEndorsement():
    print "Getting authorization token."

    #URL = "https://api.develop.socotra.com/account/authenticate"
    URL = "http://127.0.0.1:8080/account/authenticate"
    #URL = "https://api.develop.socotra.com/account/v1/authenticateInternal
    payload = {
                "username": "alice.lee",
                "password": "socotra",
                "hostName": "vishnu-vishnu1.co.develop.socotra.com"
                }

    r = requests.post(URL, json=payload)
    data = json.loads(r.text)
    authorizationToken = data["authorizationToken"]
    print("Retrieved the authorization token.")

    policyResponseURL = "https://api.develop.socotra.com/policy/100005202/"
    headers = { "content-type":"application/json" }
    headers['Authorization'] = authorizationToken

    r = requests.get(policyResponseURL, headers=headers)
    data = json.loads(r.text)
    exposures = data['exposures']
    exposureLocator = exposures[0]['locator']

    exposure = exposures[0]
    perils = exposure['perils']

    peril = perils[1]
    perilLocatorToRemove = peril['locator'].encode('ascii', 'ignore')
    perilLocatorToUpdate = perils[2]['locator'].encode('ascii', 'ignore')

    deductible = "100"
    lumpSumPayment = "200"

    perilUpdateRequest = dict([("addFieldGroups", []),
                               ("fieldValues", {}),
                               ("perilLocator", perilLocatorToUpdate),
                               ("removeFieldGroup", []),
                               ("updateFieldGroups", []),
                               ("deductible", deductible),
                               ("lumpSumPayment", lumpSumPayment),
                               ("removeIndemnityPerEvent", False),
                               ("removeIndemnityPerItem", False)])

    exposureUpdateRequest = dict([("addFieldGroups", []),
                                  ("addPerils", []),
                                  ("endPerils", []),
                                  ("exposureLocator", exposureLocator),
                                  ("fieldValues", {}),
                                  ("removeFieldGroups", []),
                                  ("updateFieldGroups", []),
                                  ("updatePerils", [perilUpdateRequest])])

    # exposureUpdateRequest = dict([("addFieldGroups", []),
    #                               ("addPerils", []),
    #                               ("endPerils", [perilLocatorToRemove]),
    #                               ("exposureLocator", exposureLocator),
    #                               ("fieldValues", {}),
    #                               ("removeFieldGroups", []),
    #                               ("updateFieldGroups", []),
    #                               ("updatePerils", [])])


    # exposureUpdateRequest = dict([("addFieldGroups", []),
    #                               ("addPerils", [{"name":"bodily_injury"}]),
    #                               ("endPerils", []),
    #                               ("exposureLocator", exposureLocator),
    #                               ("fieldValues", {}),
    #                               ("removeFieldGroups", []),
    #                               ("updateFieldGroups", []),
    #                               ("updatePerils", [])])

    policyUpdateRequest = dict([("addExposures", []),
                                ("addFieldGroups", []),
                                ("endExposures", []),
                                ("fieldValues", {}),
                                ("removeFieldGroups", []),
                                ("updateExposures", [exposureUpdateRequest]),
                                ("updateFieldGroups", []),
                                ("hasPolicyUpdates", False)])

    endorsementRequest = dict([("endorsementName", "generic"),
                               #("startTimestamp", 1564642800000),
                               ("startTimestamp", 1565852400000),
                               ("updatePolicy", policyUpdateRequest)])

    endorsementURL = "https://api.develop.socotra.com/policy/100005202/endorse"
    r = requests.post(endorsementURL, json=endorsementRequest, headers=headers)
    print(r.headers.items())
    #print(r)

    updatedPolicy = requests.get(policyResponseURL, headers=headers)
    updatedData = updatedPolicy.json()
    print(updatedData)

if __name__ == '__main__':
    perilEndorsement()
