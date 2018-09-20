import argparse
import sys
import json
from socotratools.client import SocotraClient


def is_lapsed(mods):
        i = 0
        lapse_counter = 0
        reinstate_counter = 0

        for mod in mods:
            i = i + 1
            if mod['name'] == 'modification.policy.lapse':
                lapse_counter = i
            elif mod['name'] == 'modification.policy.reinstate':
                reinstate_counter = i

        if lapse_counter > reinstate_counter:
            return True
        else:
            return False


def is_graced(glrs):

    for glr in glrs:
        graceResponse = glr['gracePeriod']
        if graceResponse.get('settledTimestamp'):
            continue
        else:
            return True
    return False


def is_finalized(mods):
    for mod in mods:
        if mod.get('automatedUnderwritingResult'):
            return True
    return False


def get_policy_status(client, policy_locator):

    policy = client.get_policy(policy_locator)
    glrs = client.get_grace_lapse_reinstatements(policy_locator)
    if is_lapsed(policy['modifications']):
        return 'lapsed'
    elif is_graced(glrs):
        return 'in grace'
    elif policy.get('cancellation'):
        cancellation = policy['cancellation']
        if cancellation['modificationName'] == 'modification.policy.withdraw':
            return 'withdrawal'
        else:
            return 'canceled'
    elif policy.get('issuedTimestamp'):
        return 'issued'
    elif is_finalized(policy['modifications']):
        return 'finalized'
    else:
        return 'created'


def main(argv):

    parser = argparse.ArgumentParser(
        description='Main Test Application')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra', required=False)
    parser.add_argument('-l', '--locator', required=True)
    args = parser.parse_args(argv)

    print 'Authenticating with tenant: ' + args.hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password)

    policy_locator = args.locator
    print get_policy_status(client, policy_locator)
    print client.get_policy_status(policy_locator)


if __name__ == "__main__":
    main(sys.argv[1:])
