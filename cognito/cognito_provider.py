import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import sys
import json
import base64
from warrant import Cognito
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class CognitoIdentity:
    """Identity implementation for adding directory services using AWS Cognito"""
    # requires:  export AWS_DEFAULT_REGION=eu-west-1


    def __init__(self, id_file):
        self.allowed_perms = []
        with open(id_file, "r") as f:
            self.identity = json.load(f)

    def get_groups(self, jwt_token):
        token_bits = jwt_token.split('.')
        # Use the jwt haader and signature to verify authenticity
        # header = token_bits[0]
        # sig = token_bits[2]

        payload = token_bits[1]
        missing_padding = len(payload) % 4
        if missing_padding != 0:
            payload += b'=' * (4 - missing_padding)
        jwt_payload = json.loads(base64.decodestring(payload))
        return jwt_payload['cognito:groups']

    def authenticate(self, username, password):
        clientId = self.identity['provider']['client_id']
        userPoolId = self.identity['provider']['userpool_id']

        u = Cognito(userPoolId, clientId, username=username)
        u.authenticate(password=password)
        # TODO: if this fails, we should error gracefully with a 401
        token = u.id_token
        self.allowed_perms = self.set_perms(token)

    def set_perms(self, token):
        perms = []
        groups = self.get_groups(token)
        roles = self.identity['roles']
        for role in roles.keys():
            if role in groups:
                perms = perms + roles[role]
        return perms

    def get_all_perms(self):
        perms = []
        roles = self.identity['roles']
        for role in roles.keys():
                perms = perms + roles[role]
        return perms

    def get_perms(self):
        return self.allowed_perms

    def check_perms(self, method_name):
        if method_name in self.allowed_perms:
            return True
        else:
            return False

    def get_soc_username(self):
            return self.identity['socotra']['username']

    def get_soc_password(self):
            return self.identity['socotra']['password']