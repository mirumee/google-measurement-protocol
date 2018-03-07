from prices import Money


def item(
        name, unit_price, quantity=None, item_id=None, category=None,
        **extra_data):
    payload = {
        't': 'item', 'in': name, 'ip': str(unit_price.amount),
        'cu': unit_price.currency}

    if quantity:
        payload['iq'] = str(int(quantity))
    if item_id:
        payload['ic'] = item_id
    if category:
        payload['iv'] = category

    payload.update(extra_data)
    return payload


def transaction(
        transaction_id, items, revenue, tax=None, shipping=None,
        affiliation=None, **extra_data):
    if not items:
        raise ValueError('You need to specify at least one item')

    payload = {
        't': 'transaction', 'ti': transaction_id, 'tr': str(revenue.amount),
        'tt': '0', 'cu': revenue.currency}

    if affiliation:
        payload['ta'] = affiliation
    if shipping is not None:
        payload['ts'] = str(shipping.amount)
    if tax is not None:
        payload['tt'] = str(tax.amount)
        
    payload.update(extra_data)
    yield payload
    
    for item in items:
        final_item = dict(item)
        final_item['ti'] = transaction_id
        yield final_item