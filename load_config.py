"""Loads a Socotra Configuration into a Socotra Tenant

After running this script you will will have a Socotra Tenant loaded
with the Configuration you provide.  This script will give you the
URL of that Tenant.  You need an administrative user+password for the
Socotra Sandbox Environment / Socotra Config Studio.

Usage
-----
$ python load_config.py --help

Python 3
--------
This script now requires Python 3.6+

Required Packages
-----------------
This script requires the following packages to be installed within the
Python environment you are running this script in:
- requests

Reference
---------
Socotra Configuration: https://docs.socotra.com/production/configuration/walkthrough.html
configuration/deployTest endpoint: https://docs.socotra.com/production/api/configuration.html

Problems and Improvements
-------------------------
This script is maintained by Will Barley, will.barley@socotra.com
Reach out!
support@socotra.com for *quick support*
will.barley@socotra.com to talk directly to the maintainer
Or open an new issue in the repository:
https://github.com/socotra/public/issues/new?title=issue%20with%20load_config.py


Development
-----------
Conventional Commits: https://www.conventionalcommits.org/
Black for deterministic code formatting: https://black.readthedocs.io/

"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from shutil import make_archive
from typing import Union

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

SANDBOX_URL = "https://api.sandbox.socotra.com"


class BetterArgParser(argparse.ArgumentParser):
    """Extension to ArgumentParser that prints the usage statement alongside any error"""

    def error(self, message):
        """Prints the script's usage statement and then the typical error message"""
        self.print_help()
        super().error(message)


def get_arguments() -> object:
    """Gets arguments from the command line

    Returns
    -------
    argparse.Namespace
        The arguments collected from the command line
    """

    parser = BetterArgParser(
        description="Load Socotra Configuration into a Socotra Tenant."
    )
    parser.add_argument(
        "--tenant_suffix",
        "-t",
        help="This will be used to create the hostname of your tenant as follows: "
        "<username>-<tenant_suffix>.co.sandbox.socotra.com. "
        "Note: 'configeditor' is not allowed.",
        required=True,
    )
    parser.add_argument(
        "--folder",
        "-f",
        help="The path of the root folder of your Socotra Config that you want to load.",
        required=True,
    )
    parser.add_argument(
        "--username",
        "-u",
        help="Socotra Config Studio username. "
        "Uses SOCOTRA_USERNAME env variable if not provided.",
        required=False,
    )
    parser.add_argument(
        "--password",
        "-p",
        help="Socotra Config Studio password. "
        "Uses SOCOTRA_PASSWORD env variable if not provided.",
        required=False,
    )
    parser.add_argument(
        "--debug", "-d", help="prints debugging info", action="store_true"
    )

    arg = parser.parse_args()

    if arg.username is None:
        try:
            arg.username = os.environ["SOCOTRA_USERNAME"]
        except KeyError:
            parser.error(
                "No --username provided "
                "and no SOCOTRA_USERNAME environment variable found"
            )

    if arg.password is None:
        try:
            arg.password = os.environ["SOCOTRA_PASSWORD"]
        except KeyError:
            parser.error(
                "No --password provided "
                "and no SOCOTRA_PASSWORD environment variable found"
            )

    arg.folder = str(Path(arg.folder).resolve())
    return arg


def post_zip_to_server(
    file: Union[str, Path],
    tenant_suffix: str,
    username: str,
    password: str,
    debug: bool = True,
) -> None:
    """Loads a zipped Socotra Configuration into a Tenant.

    Parameters
    ----------
    file
        The path to the zip file containing the Socotra Configuration
    tenant_suffix
        The suffix to use to create the hostname of your target Tenant
    username
    password
    debug

    Examples
    --------
    Bad User/Password
    >>> post_zip_to_server('/tmp/file.zip', 'tenant12', 'user', 'pass')
    Traceback (most recent call last):
        ...
    ValueError: HTTP 401: Unauthorized: Could not authenticate with the provided username and password.
    """

    # Authenticate
    token = get_auth_token(username, password, debug=debug)

    # Construct the Request
    auth_header = {"Authorization": token}
    post_data = {"tenantNameSuffix": tenant_suffix}
    url = SANDBOX_URL + "/configuration/deployTest"
    with open(str(file), mode="rb") as binary_data:
        file_data = {"zipFile": binary_data}
        response = requests.post(
            url, post_data, files=file_data, verify=False, headers=auth_header
        )

    try:
        json_response = json.loads(response.text)
    except ValueError:
        print("An error happened!\n")
        print("Headers: %s" % response.headers)
        print("Status Code: %s" % response.status_code)
        print("Data: %s" % response.text)
        return

    if json_response.get("success"):
        print("============== load was successful ==============")
        print(f"hostname: {json_response['hostname']}")
        print(f"url: https://{json_response['hostname']}")

    else:
        print("============== load failed ==============")
        log = json_response.get("logfile")
        if log:
            print(f"Loading Log:\n {log}")
        else:
            print(f"Loading Response:\n {json_response}")


def get_auth_token(username, password, debug: bool = False):
    """Get an Authorization Token for the user and password.

    Parameters
    ----------
    username
    password
    debug
        Print debug messages

    Returns
    -------
    str
        The Authorization token

    """
    post_data = {"username": username, "password": password}
    auth_url = SANDBOX_URL + "/account/authenticate"
    r = requests.post(auth_url, json=post_data, verify=False)
    json_response = json.loads(r.text)
    log_debug(f"Response from load: {json_response}", debug)

    token = json_response.get("authorizationToken")
    if token:
        return token

    status = json_response.get("httpStatus")
    if status == "401":
        raise ValueError(
            f"HTTP {status}: Unauthorized: Could not authenticate with "
            f"the provided username and password."
        )
    raise ValueError(
        f"HTTP {status}: There was some sort of problem while trying to "
        f"authenticate the user and password."
    )


def log_debug(message: str, debug: bool = False):
    """Print out debug messages if the `debug` parameter is True"""
    if debug:
        print(message)


def main():
    """Main! Executed when this script is run from the command line.

    Examples
    --------
    Simulate: $ python load_config.py -t myTenant -f . -u myUser -p myPass
    >>> import sys
    >>> sys.argv = ['load_config.py', '-t', 'myTenant', '-f', '.', '-u', 'myUser', '-p', 'myPass']
    >>> main()
    Traceback (most recent call last):
        ...
    ValueError: HTTP 401: Unauthorized: Could not authenticate with the provided username and password.
    """
    args = get_arguments()
    log_debug(f"Arguments: {args}", args.debug)

    # Create a temporary directory (that will work on any operating system)
    #  where we will create our zip file, and clean it up when done
    with tempfile.TemporaryDirectory() as dir_name:
        d = Path(dir_name)  # turn into a Path object
        log_debug(f"Created temporary directory: {d}", args.debug)

        print("Zipping")
        log_debug(f"Zipping up: {args.folder}", args.debug)
        zipped = make_archive(
            base_name=d / "archive", format="zip", root_dir=args.folder
        )
        log_debug(f"Zipped to: {zipped}", args.debug)

        print("Uploading")
        post_zip_to_server(
            zipped, args.tenant_suffix, args.username, args.password, debug=args.debug
        )

        log_debug(
            f"Finishing with temporary directory, which will be removed: {d}",
            args.debug,
        )


if __name__ == "__main__":
    main()
