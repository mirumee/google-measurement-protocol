def item(
        name, unit_price, quantity=None, item_id=None, category=None,
        **extra_info):
    payload = {
        't': 'item', 'in': name, 'ip': str(unit_price.gross.amount),
        'cu': unit_price.currency}

    if quantity:
        payload['iq'] = str(int(quantity))
    if item_id:
        payload['ic'] = item_id
    if category:
        payload['iv'] = category

    payload.update(extra_info)
    return payload


def transaction(
        transaction_id, items, revenue, shipping=None, affiliation=None,
        **extra_info):
    if not items:
        raise ValueError('You need to specify at least one item')

    payload = {
        't': 'transaction', 'ti': transaction_id,
        'tr': str(revenue.gross.amount), 'tt': str(revenue.tax.amount),
        'cu': revenue.currency}

    if affiliation:
        payload['ta'] = affiliation
    if shipping is not None:
        payload['ts'] = str(shipping.gross.amount)

    payload.update(extra_info)
    yield payload
    
    for item in items:
        final_item = dict(item)
        final_item['ti'] = transaction_id
        yield final_item