import argparse
import json
import sys
from socotratools.client import SocotraClient
import stripe

# Sample application to pay all invoices from a policyholder using Stripe

# Stripe Test Key from: https://stripe.com/docs/api/python#authentication
stripe.api_key = 'sk_test_BQokikJOvBiI2HlWgH4olfQ2'

# Using temp hash map for stripe customer db as example
stripe_customers = {}


# Uses the Socotra policyholder and looks up the existing Stripe customer
# id or generates a new Stripe customer.   Also returns the display friendly
# policyholder id
def get_stripe_customer(client, ph_locator):
    # Legacy policyholder_id structure
    ph = client.get_policyholder(ph_locator)
    ph_id = ph['entity']['values']['policyholder_id'][0]

    if ph_id in stripe_customers.keys():
        customer_id = stripe_customers[ph_id]
    else:
        print 'Creating Stripe account and storing token'
        customer = stripe.Customer.create(source='tok_mastercard')
        stripe_customers[ph_id] = customer.id
        customer_id = customer.id

    return customer_id, ph_id


def main(argv):

    parser = argparse.ArgumentParser(
        description='Pay Invoice')
    parser.add_argument('-n', '--hostname', required=True)
    parser.add_argument('-u', '--username',
                        default='alice.lee', required=False)
    parser.add_argument('-p', '--password', default='socotra', required=False)
    parser.add_argument('-ph', '--ph_locator', required=True)
    args = parser.parse_args(argv)

    print 'Authenticating with tenant: ' + args.hostname
    client = SocotraClient.get_authenticated_client_for_hostname(
        args.hostname, args.username, args.password)

    ph_locator = args.ph_locator
    customer_id, ph_id = get_stripe_customer(client, ph_locator)

    # Iterate through all invoices for this policyholder
    invoices = client.get_invoices_for_policyholder(ph_locator)
    for invoice in invoices:
        # Only worry about outstanding invoices that aren't paid yet.
        if invoice['settlementStatus'] == 'outstanding':
            amount = int(float(invoice['totalDue']) * 100)
            # Try to charge stripe for this invoice
            charge = stripe.Charge.create(
                amount=amount,
                currency=invoice['totalDueCurrency'],
                customer=customer_id
            )
            if charge['status'] == 'succeeded':
                # if Stripe succeeded, mark the invoice paid in Socotra
                client.pay_invoice(invoice['locator'])
                print 'Invoice paid for policyholder ' + ph_id + \
                    ' regarding invoice ' + invoice['displayId']
            else:
                print 'Stripe payment failed'


if __name__ == "__main__":
    main(sys.argv[1:])
