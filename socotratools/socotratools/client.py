import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import sys
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class SocotraClient:
    """Http client for connecting to Socotra"""

    def __init__(self, base_url, debug=False):
        self.base_url = base_url
        self.debug = debug
        self.session = requests.session()
        self.perms = []

    def __debug(self, string):
        if self.debug:
            if type(string) == dict:
                print json.dumps(string)
            else:
                print string

    # Used for permissions
    def is_allowed(self, method_name):
        always_allowed = ['authenticate', 'renew']

        if self.perms == 'ALL':
            allowed = True
        elif method_name in always_allowed:
            allowed = True
        elif method_name in self.perms:
            allowed = True
        else:
            allowed = False

        return allowed

    def __get(self, resource, params=None):

        caller = sys._getframe(1).f_code.co_name
        if self.is_allowed(caller):
            url = self.base_url + resource
            self.__debug('GET: ' + url)
            r = self.session.get(url, params=params, verify=False)
            status = r.status_code
            self.__debug('Return status: ' + str(status))
            value = r.json()
            self.__debug('Return body: \n')
            self.__debug(value)
            return value
        else:
            self.__debug('Unathorized operation: ' + caller)
            return {'Error 403': 'Unauthorized for ' + caller}

    def __post(self, resource, payload=None, data=None, files=None):

        caller = sys._getframe(1).f_code.co_name
        if self.is_allowed(caller):
            url = self.base_url + resource
            self.__debug('POST: ' + url)
            self.__debug('Request:')
            self.__debug(payload)
            r = self.session.post(url, json=payload, data=data,
                                  verify=False, files=files)
            status = r.status_code
            self.__debug('Return status: ' + str(status))
            value = r.json()
            self.__debug('Return body: \n')
            self.__debug(value)
            return value
        else:
            self.__debug('Unathorized operation: ' + caller)
            return {'Error 403': 'Unauthorized for ' + caller}

    def __patch(self, resource, payload=None, data=None, files=None):

        caller = sys._getframe(1).f_code.co_name
        if self.is_allowed(caller):
            url = self.base_url + resource
            self.__debug('PATCH: ' + url)
            self.__debug('Request:')
            self.__debug(payload)
            r = self.session.patch(url, json=payload, data=data,
                                   verify=False, files=files)
            status = r.status_code
            self.__debug('Return status: ' + str(status))
            value = r.json()
            self.__debug('Return body: \n')
            self.__debug(value)
            return value
        else:
            self.__debug('Unathorized operation: ' + caller)
            return {'Error 403': 'Unauthorized for ' + caller}

    def __validate_unauthenticated(self):
        if "Authorization" in self.session.headers.keys():
            raise Exception(
                'Client already authenticated. Please create a new client and authenticate again')

    @classmethod
    def get_authenticated_client_for_hostname(cls, host_name, username, password, api_url=None, debug=False, identity=None):
        if api_url is None:
            api_url = cls.__get_api_url_from_host_name(host_name)
        client = cls(api_url, debug=debug)
        client.authenticate(username, password,
                            host_name=host_name, identity=identity)
        return client

    @classmethod
    def get_authenticated_client_from_token(cls, token, api_url=None, debug=False, identity=None):
        client = cls(api_url, debug=debug)
        client.authenticate_from_token(token, identity=identity)
        return client

    @staticmethod
    def __get_api_url_from_host_name(host_name):
        host_pieces = host_name.strip().split('.')
        environment_name = host_pieces[-3]
        if environment_name != "api":
            return "https://api." + environment_name + ".socotra.com"
        else:
            return "https://api.socotra.com"

    def authenticate(self, username, password, tenant_name=None, host_name=None, identity=None):
        self.__validate_unauthenticated()
        if identity is not None:
            identity.authenticate(username, password)
            username = identity.get_soc_username()
            password = identity.get_soc_password()
            self.perms = identity.get_perms()
        else:
            self.perms = 'ALL'

        data = {
            'username': username,
            'password': password,
            'tenantName': tenant_name,
            'hostName': host_name
        }
        return_value = self.__post('/account/authenticate', data)
        self.session.headers.update({
            "Authorization": return_value['authorizationToken'],
            "Socotra-Forced-Flags": "property.endorsement.renewal.underwriting.enabled=true"
        })
        return return_value

    def authenticate_from_token(self, token, identity=None):
        self.__validate_unauthenticated()
        if identity is not None:
            identity.authenticate(username, password)
            username = identity.get_soc_username()
            password = identity.get_soc_password()
            self.perms = identity.get_perms()
        else:
            self.perms = 'ALL'

        self.session.headers.update({
            "Authorization": token,
            "Socotra-Forced-Flags": "property.endorsement.renewal.underwriting.enabled=true"
        })
        return self.renew()

    def renew(self):
        return_value = self.__post('/account/renewAuthentication')
        self.session.headers.update(
            {"Authorization": return_value['authorizationToken']})
        return return_value

    @classmethod
    def get_authenticated_client_from_token(cls, token, api_url=None, debug=False, identity=None):
        client = cls(api_url, debug=debug)
        client.authenticate_from_token(token, identity=identity)
        return client

    def authenticate_from_token(self, token, identity=None):
        self.__validate_unauthenticated()
        if identity is not None:
            identity.authenticate(username, password)
            username = identity.get_soc_username()
            password = identity.get_soc_password()
            self.perms = identity.get_perms()
        else:
            self.perms = 'ALL'

        self.session.headers.update({
            "Authorization": token
        })
        return self.renew()

    def get_all_policyholders(self,
                              start_timestamp=None,
                              end_timestamp=None,
                              page_size=None,
                              paging_token=None):
        data = {
            "createdAfterTimestamp": start_timestamp,
            "createdBeforeTimestamp": end_timestamp,
            "pageSize": page_size,
            "pagingToken": paging_token
        }
        return self.__get("/policyholders", data)

    def get_policyholder(self, locator):
        return self.__get("/policyholder/" + locator)

    def create_policyholder(self, completed=True, values=None, sub_entities=None):
        data = {
            'completed': completed,
            'values': values,
            'subEntities': sub_entities
        }
        return self.__post('/policyholder/create', data)

    def update_policyholder(
            self,
            locator,
            version,
            completed,
            values=None,
            add_sub_entities=None,
            update_sub_entities=None,
            delete_sub_entities=None):
        data = {
            "locator": locator,
            "version": version,
            "completed": completed,
            "values": values,
            "addSubEntities": add_sub_entities,
            "updateSubEntities": update_sub_entities,
            "deleteSubEntities": delete_sub_entities
        }
        return self.__post('/policyholder/update', data)

    def get_policies_for_policyholder(self, locator):
        return self.__get("/policyholder/{0}/policies".format(locator))

    def get_invoices_for_policyholder(self, locator):
        return self.__get("/policyholder/{0}/invoices".format(locator))

    def create_policy(self,
                      product_name,
                      policyholder_locator,
                      policy_start_timestamp,
                      policy_end_timestamp,
                      field_values={},
                      field_groups=[],
                      exposures=[],
                      finalize=True):
        data = {
            'productName': product_name,
            'policyholderLocator': policyholder_locator,
            'policyStartTimestamp': policy_start_timestamp,
            'policyEndTimestamp': policy_end_timestamp,
            'fieldValues': field_values,
            'fieldGroups': field_groups,
            'exposures': exposures,
            'finalize': finalize
        }
        return self.__post('/policy/', data)

    def get_policy(self, locator):
        url = '/policy/' + locator
        return self.__get(url)

    def update_policy(self,
                      policy_locator,
                      field_values={},
                      add_field_groups=[],
                      update_field_groups=[],
                      remove_field_groups=[],
                      add_exposures=[],
                      update_exposures=[],
                      remove_exposures=[],
                      policy_start_timestamp=None,
                      policy_end_timestamp=None):
        data = {
            'policyLocator': policy_locator,
            'fieldValues': field_values,
            'addFieldGroups': add_field_groups,
            'updateFieldGroups': update_field_groups,
            'removeFieldGroups': remove_field_groups,
            'addExposures': add_exposures,
            'updateExposures': update_exposures,
            'removeExposures': remove_exposures,
            'policyStartTimestamp': policy_start_timestamp,
            'policyEndTimestamp': policy_end_timestamp
        }
        return self.__post('/policy/' + policy_locator + '/update', data)

    def finalize_policy(self, locator):
        return self.__post('/policy/{0}/finalize'.format(locator))

    def issue_policy(self, locator):
        return self.__post('/policy/{0}/issue'.format(locator))

    def cancel_policy(self, locator, end_timestamp):
        return self.__post(
            '/policy/{0}/cancel'.format(locator),
            {"coverageEndTimestamp": end_timestamp})

    def get_events(
            self,
            start_timestamp=None,
            end_timestamp=None,
            page_size=None,
            paging_token=None):
        data = {
            "startTimestamp": start_timestamp,
            "endTimestamp": end_timestamp,
            "pageSize": page_size,
            "pagingToken": paging_token
        }
        return self.__get("/eventstream/events", data)

    def get_products(self):
        return self.__get("/products")

    def upload_media(self, file_name, file):
        return self.__post("/media/?fileName=" + file_name, files={"file": file})

    def get_media(self, locator):
        return self.__get("/media/" + locator)

    def pay_invoice(self, locator, field_values={}):
        data = {
            "fieldValues": field_values
        }
        return self.__post('/invoice/' + locator + '/pay', data)

    def get_invoice_ftrs(self, locator):
        return self.__get('/invoice/' + locator + '/financialTransactions')

    def check_existing_peril_premium(self, calculation, peril_id):
        data = {"calculation": calculation, "perilDisplayId": peril_id}
        return self.__post("/calculation/checkExistingPerilPremium", data)

    def check_peril_premium(
            self,
            product_name,
            calculation,
            policy_characteristics,
            exposure_name,
            exposure_characteristics,
            peril_name,
            peril_characteristics):
        data = {
            "calculation": calculation,
            "productName": product_name,
            "policyCharacteristics": policy_characteristics,
            "exposureName": exposure_name,
            "exposureCharacteristics": exposure_characteristics,
            "perilName": peril_name,
            "perilCharacteristics": peril_characteristics
        }
        return self.__post("/calculation/checkPerilPremium", data)

    def render_policy_document(self, policy_display_id, template):
        data = {
            "template": template,
            "policyDisplayId": policy_display_id
        }
        return self.__post("/document/renderPolicyDocument", data)

    def add_document_to_policy(self, policy_locator, display_name, document_type, document):
        data = {
            "displayName": display_name,
            "documentType": document_type
        }
        return self.__post(
            "/policy/" + policy_locator + "/addDocument", data=data, files={"document": document})

    def remove_document_from_policy(self, policy_locator, document_locator):
        data = {
            "documentLocator": document_locator
        }
        return self.__post("/policy/" + policy_locator + "/removeDocument", data)

    def price_policy(self, locator):
        return self.__post("/policy/" + locator + "/price")

    def uw_policy(self, locator):
        return self.__get("/policy/" + locator + "/automatedUnderwritingResult")

    def preview_endorsement_price(self, policy_locator, endorsement_name,
                                  effective_timestamp, end_timestamp=None,
                                  field_values={}, add_field_groups=[],
                                  update_field_groups=[], remove_field_groups=[],
                                  add_exposures=[], update_exposures=[],
                                  end_exposures=[]):

        update_request = {
            "fieldValues": field_values,
            "addFieldGroups": add_field_groups,
            "updateFieldGroups": update_field_groups,
            "removeFieldGroups": remove_field_groups,
            "addExposures": add_exposures,
            "updateExposures": update_exposures,
            "endExposures": end_exposures
        }
        data = {'endorsementName': endorsement_name,
                'startTimestamp': effective_timestamp,
                'newPolicyEndTimestamp': end_timestamp,
                'updatePolicy': update_request
                }

        return self.__post("/policy/" + policy_locator + "/previewEndorsementPrice", data)

    def endorse(self, policy_locator, endorsement_name,
                effective_timestamp, end_timestamp=None,
                field_values={}, add_field_groups=[],
                update_field_groups=[], remove_field_groups=[],
                add_exposures=[], update_exposures=[],
                end_exposures=[]):

        update_request = {
            "fieldValues": field_values,
            "addFieldGroups": add_field_groups,
            "updateFieldGroups": update_field_groups,
            "removeFieldGroups": remove_field_groups,
            "addExposures": add_exposures,
            "updateExposures": update_exposures,
            "endExposures": end_exposures
        }
        data = {'endorsementName': endorsement_name,
                'startTimestamp': effective_timestamp,
                'newPolicyEndTimestamp': end_timestamp,
                'updatePolicy': update_request
                }

        return self.__post("/policy/" + policy_locator + "/endorse", data)

    def generate_report(self, report_name,
                        report_timestamp, end_timestamp=None):
        if end_timestamp is None:
            data = {'reportTimestamp': report_timestamp
                    }
        else:
            data = {'startTimestamp': report_timestamp,
                    'endTimestamp': end_timestamp
                    }

        return self.__post("/report/" + report_name, data)

    def get_report(self, locator):
        return self.__get("/report/" + locator + "/status")

    def get_locator(self, display_id):
        data = {'displayId': display_id}
        return self.__get("/policy/locator", params=data)

    def get_grace_lapse_reinstatements(self, locator):
        return self.__get(
            "/policy/{0}/graceLapseReinstatements".format(locator))

    def is_lapsed(self, modifications):
        i = 0
        lapse_counter = 0
        reinstate_counter = 0

        for mod in modifications:
            i = i + 1
            if mod['name'] == 'modification.policy.lapse':
                lapse_counter = i
            elif mod['name'] == 'modification.policy.reinstate':
                reinstate_counter = i

        if lapse_counter > reinstate_counter:
            return True
        else:
            return False

    def is_in_grace(self, glrs):

        for glr in glrs:
            graceResponse = glr['gracePeriod']
            if graceResponse.get('settledTimestamp'):
                continue
            else:
                return True
        return False

    def is_finalized(self, modifications):
        for mod in modifications:
            if mod.get('automatedUnderwritingResult'):
                return True
        return False

    def get_policy_status(self, policy_locator):

        policy = self.get_policy(policy_locator)
        glrs = self.get_grace_lapse_reinstatements(policy_locator)
        if self.is_lapsed(policy['modifications']):
            return 'lapsed'
        elif self.is_in_grace(glrs):
            return 'in grace'
        elif policy.get('cancellation'):
            cancellation = policy['cancellation']
            if cancellation['modificationName'] == 'modification.policy.withdraw':
                return 'withdrawal'
            else:
                return 'canceled'
        elif policy.get('issuedTimestamp'):
            return 'issued'
        elif self.is_finalized(policy['modifications']):
            return 'finalized'
        else:
            return 'created'

<<<<<<< HEAD
    def create_endorsement(self, policy_locator, endorsement_name,
                           effective_timestamp=None,
                           field_values=None,
                           add_field_groups=None,
                           remove_field_groups=None,
                           update_field_groups=None,
                           add_exposures=None,
                           end_exposures=None,
                           update_exposures=None,
                           end_timestamp=None,
                           # above: optional
                           state='application'):
        data = {'endorsementName': endorsement_name,
                'startTimestamp': effective_timestamp,
                'fieldValues': field_values,
                'addFieldGroups': add_field_groups,
                'removeFieldGroups': remove_field_groups,
                'updateFieldGroups': update_field_groups,
                'addExposures': add_exposures,
                'endExposures': end_exposures,
                'updateExposures': update_exposures,
                'newPolicyEndTimestamp': end_timestamp,
                'state': state}
        return self.__post("/policies/" + policy_locator +
                           "/endorsements", data)

    def update_endorsement(self, endorsement_locator,
                           effective_timestamp=None,
                           field_values=None,
                           add_field_groups=None,
                           remove_field_groups=None,
                           update_field_groups=None,
                           add_exposures=None,
                           end_exposures=None,
                           update_exposures=None,
                           end_timestamp=None,
                           # above: optional
                           action='update'):
        affects_exposures = add_exposures or end_exposures or update_exposures  # alias end/remove_exposures?
        affects_fields = field_values or add_field_groups or remove_field_groups or update_field_groups
        endorsement_update = None if not (end_timestamp or affects_exposures or affects_fields) else {
            'startTimestamp': effective_timestamp,
            'fieldValues': field_values,
            'addFieldGroups': add_field_groups,
            'removeFieldGroups': remove_field_groups,
            'updateFieldGroups': update_field_groups,
            'addExposures': add_exposures,
            'endExposures': end_exposures,
            'updateExposures': update_exposures,
            'newPolicyEndTimestamp': end_timestamp,
        }
        data = {'action': action, 'endorsementUpdate': endorsement_update}
        return self.__patch("/endorsements/" + endorsement_locator, data)

    def get_endorsement(self, endorsement_locator):

        return self.__get("/endorsements/" + endorsement_locator)

    def uw_endorsement(self, endorsement_locator):

        return self.__get("/endorsements/" + endorsement_locator +
                          "/automatedUnderwritingResult")

    def price_endorsement(self, endorsement_locator):

        return self.__get("/endorsements/" + endorsement_locator + "/price")

    def get_endorsements_from_policy(self, policy_locator):

        return self.__get("/policies/" + policy_locator +
                          "/endorsements")

    def create_renewal(self, policy_locator,
                       field_values=None,
                       add_field_groups=None,
                       remove_field_groups=None,
                       update_field_groups=None,
                       add_exposures=None,
                       end_exposures=None,
                       update_exposures=None,
                       # above: optional
                       end_timestamp=None,
                       state='application'):
        data = {
                'fieldValues': field_values,
                'addFieldGroups': add_field_groups,
                'updateFieldGroups': update_field_groups,
                'removeFieldGroups': remove_field_groups,
                'addExposures': add_exposures,
                'updateExposures': update_exposures,
                'endExposures': end_exposures,
                'renewalEndTimestamp': end_timestamp,
                'state': state}
        return self.__post("/policies/" + policy_locator +
                           "/renewals", data)

    def update_renewal(self, renewal_locator,
                       field_values=None,
                       add_field_groups=None,
                       remove_field_groups=None,
                       update_field_groups=None,
                       add_exposures=None,
                       end_exposures=None,
                       update_exposures=None,
                       end_timestamp=None,
                       # above: optional
                       action='update'):
        affects_exposures = add_exposures or end_exposures or update_exposures  # alias end/remove_exposures?
        affects_fields = field_values or add_field_groups or remove_field_groups or update_field_groups
        renewal_update = None if not (end_timestamp or affects_exposures or affects_fields) else {
            'fieldValues': field_values,
            'addFieldGroups': add_field_groups,
            'updateFieldGroups': update_field_groups,
            'removeFieldGroups': remove_field_groups,
            'addExposures': add_exposures,
            'updateExposures': update_exposures,
            'endExposures': end_exposures,
            'renewalEndTimestamp': end_timestamp,
        }
        data = {'action': action, 'renewalUpdate': renewal_update}
        return self.__patch("/renewals/" + renewal_locator, data)

    def get_renewal(self, renewal_locator):

        return self.__get("/renewals/" + renewal_locator)

    def uw_renewal(self, renewal_locator):

        return self.__get("/renewals/" + renewal_locator +
                          "/automatedUnderwritingResult")

    def price_renewal(self, renewal_locator):

        return self.__get("/renewals/" + renewal_locator + "/price")

    def get_renewals_from_policy(self, policy_locator):

        return self.__get("/policies/" + policy_locator +
                          "/renewals")

    def get_claims(self,
                   start_timestamp=None,
                   end_timestamp=None,
                   page_size=None,
                   paging_token=None):

        data = {
            "createdAfterTimestamp": start_timestamp,
            "createdBeforeTimestamp": end_timestamp,
            "pageSize": page_size,
            "pagingToken": paging_token
        }
        return self.__get("/claims", data)

    def get_claim(self, locator):
        url = '/claim/' + locator
        return self.__get(url)

    def create_claim(self, locator,
                     field_groups=[],
                     field_values={},
                     incident_timestamp=None,
                     notification_timestamp=None,
                     status=None):

        data = {
            "fieldGroups": field_groups,
            "fieldValues": field_values,
            "policyLocator": locator,
            "incidentTimestamp": incident_timestamp,
            "notificationTimestamp": notification_timestamp,
            "status": status
        }
        url = '/claim'
        return self.__post(url, data)

    def update_claim(self, locator, add_field_groups=[],
                     add_subclaims=[], field_values={},
                     remove_field_groups=[], update_field_groups=[],
                     update_subclaims=[],
                     incident_timestamp=None,
                     notification_timestamp=None,
                     status=None):

        data = {
            "addFieldGroups": add_field_groups,
            "addSubClaims": add_subclaims,
            "fieldValues": field_values,
            "removeFieldGroups": remove_field_groups,
            "updateFieldGroups": update_field_groups,
            "updateSubClaims": update_subclaims,
            "incidentTimestamp": incident_timestamp,
            "notificationTimestamp": notification_timestamp,

        }
        url = '/claim/' + locator + '/update'
        return self.__post(url, data)

    def discard_claim(self, locator):
        url = '/claim/' + locator + '/discard'
        return self.__post(url)

    def get_payable(self, locator):
        url = '/claims/payables/' + locator
        return self.__get(url)

    def reverse_payable(self, locator, comment=None):
        data = {
            "payableLocator": locator,
            "comment": comment
        }
        url = '/claims/payables/reversals'
        return self.__post(url, data)
