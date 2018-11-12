#!/usr/bin/env python
import os
import zipfile
import requests
import json
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# This script can be used to load Socotra configuration into a test instance.
# Execute the script from the root folder of the configuration you wish to
# upload.

# designed for UNIX file systems - change to c:\TEMP for Windows systems
ZIPFILE = '/tmp/tenant.zip'
base_url = 'https://api.sandbox.socotra.com'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Load Socotra Configuration')
    parser.add_argument('--tenant_name', '-t',
                        help='The suffix of the tenant - \
                        configeditor is not allowed',
                        required=True)
    parser.add_argument('--username', '-u',
                        help='Socotra Config Studio username \
                        uses SOCOTRA_USERNAME env variable if \
                        not provided',
                        required=False)
    parser.add_argument('--password', '-p',
                        help='Socotra Config Studio password - \
                        uses SOCOTRA_PASSWORD env variable if \
                        not provided',
                        required=False)
    parser.add_argument(
        '--debug', '-d', help="prints debugging info", action='store_true')
    return parser.parse_args()


def create_zip_from_assets():
    with zipfile.ZipFile(ZIPFILE, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        dir_path = os.getcwd()
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if not file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    write_path = os.path.relpath(file_path, dir_path)
                    zip_file.write(file_path, write_path)


def post_zip_to_server(tenant_name, username, password):
    token = get_auth_token(username, password)
    auth_header = {'Authorization': token}
    post_data = {"tenantNameSuffix": tenant_name}
    file_data = {'zipFile': open(ZIPFILE)}
    url = base_url + '/configuration/deployTest'
    r = requests.post(url, post_data, files=file_data,
                      verify=False, headers=auth_header)
    return r


def get_auth_token(username, password):
    post_data = {"username": username,
                 "password": password}
    auth_url = base_url + '/account/authenticate'
    r = requests.post(auth_url, json=post_data, verify=False)
    json_response = json.loads(r.text)
    return json_response['authorizationToken']


def parse_response(response, debug):
    try:
        json_response = json.loads(response.text)
    except ValueError:
        print 'An error happened!\n'
        print 'Headers: %s' % response.headers
        print 'Status Code: %s' % response.status_code
        print 'Data: %s' % response.text
        return
    if debug is True:
        print json_response
        print response.text

    if json_response.get('success'):
        print "============== load was successful =============="
        print json_response['hostname']
    else:
        print "============== load failed =============="


if __name__ == '__main__':
    args = parse_args()
    create_zip_from_assets()
    if args.username is None:
        username = os.environ['SOCOTRA_USERNAME']
    else:
        username = args.username

    if args.password is None:
        password = os.environ['SOCOTRA_PASSWORD']
    else:
        password = args.password

    response = post_zip_to_server(args.tenant_name,
                                  username, password)
    parse_response(response, args.debug)
