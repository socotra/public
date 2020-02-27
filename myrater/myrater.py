
# This file is an example of Socotra's default rating
# that ships with Configuration Studio.  Instead of
# implementing the logic in Liquid, this rating algorithm
# generates the same values for each peril type


# Claims factor - This method is used multiple times
# in the pricing algorithms below.

def get_claims_multiplier(history):
    if history == '1':
        claims_multiplier = 2
    elif history == '2':
        claims_multiplier = 3
    elif history == '3':
        claims_multiplier = 4
    elif history == 'More than 3':
        claims_multiplier = 5
    else:
        claims_multiplier = 1

    return claims_multiplier


# Indemnity Adustment factor - used in multiple
# pricing algorithms below

def get_adj(indem, factor):
    adj = 0
    if indem > 0:
        adj = indem - 100000
        if adj < 0:
            adj = 0
        adj = adj * factor
    return adj


# Method that replaces the table lookup in the
# Liquid logic

def get_vehicle_type_factor(vehicle_type):
    if vehicle_type == 'Car':
        return 1
    elif vehicle_type == 'SUV':
        return 1.1
    elif vehicle_type == 'Motorcycle':
        return 2
    elif vehicle_type == 'Pickup':
        return 1.1

# This method extracts the various chraacteristics and objects
# from the contxt (data) and uses it to calculate a premium


def price_peril(data):

    current_policy_char = data['current_policy_char']
    current_exposure = data['current_exposure']
    current_exp_char = data['current_exp_char']
    current_peril = data['current_peril']
    current_peril_char = data['current_peril_char']
    peril_name = current_peril['name']

    exp_v = current_exp_char['fieldValues']
    policy_v = current_policy_char['fieldValues']

    vehicle_value = int(exp_v['vehicle_value'][0])

    if peril_name == 'a_third_party_liability':
        premium = vehicle_value * 0.021

        vehicle_type_rate = get_vehicle_type_factor(
            exp_v['vehicle_type'][0])
        premium = premium * vehicle_type_rate

        claims_multiplier = get_claims_multiplier(
            policy_v['atfault_claims_past_5_years'][0])

        premium = premium * claims_multiplier
        if policy_v['channel'][0] == 'Direct':
            premium = 0.9 * premium
        adj = get_adj(float(current_peril_char.get(
            'indemnityInAggregate', '0')), 0.002)
        premium = premium + adj
    elif peril_name == 'collision':
        premium = vehicle_value * 0.0119

        vehicle_type_rate = get_vehicle_type_factor(
            exp_v['vehicle_type'][0])
        premium = premium * vehicle_type_rate

        if policy_v['channel'][0] == 'Direct':
            premium = 0.9 * premium

    elif peril_name == 'bodily_injury':
        premium = vehicle_value * 0.0259

        vehicle_type_rate = get_vehicle_type_factor(
            exp_v['vehicle_type'][0])
        premium = premium * vehicle_type_rate

        if policy_v['channel'][0] == 'Direct':
            premium = 0.9 * premium

    elif peril_name == 'comprehensive':
        premium = 6000 * 0.0259

        vehicle_type_rate = get_vehicle_type_factor(
            exp_v['vehicle_type'][0])
        premium = premium * vehicle_type_rate

        if policy_v['channel'][0] == 'Direct':
            premium = 0.9 * premium

    elif peril_name == 'roadside_service':
        premium = 25

    elif peril_name == 'uninsured_motorist':
        premium = 19.88
        if policy_v['channel'][0] == 'Direct':
            premium = 0.9 * premium
        if policy_v['channel'][0] == 'Agent':
            premium = premium * 1.4444

        premium = premium * 0.30
        adj = get_adj(float(current_peril_char.get(
            'indemnityInAggregate', '0')), 0.150)
        premium = premium + adj

    elif peril_name == 'underinsured_motorist':
        premium = 37.33 * 0.89
        if policy_v['channel'][0] == 'Direct':
            premium = premium * 0.75
        if policy_v['channel'][0] == 'Agent':
            premium = premium * 0.9

        adj = get_adj(float(current_peril_char.get(
            'indemnityInAggregate', '0')), 0.002)
        premium = premium + adj

    premium = round(premium, 2)
    return premium
