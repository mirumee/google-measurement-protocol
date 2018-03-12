from .event import event


def enhanced_item(
        name, unit_price, quantity=None, item_id=None, category=None,
        brand=None, variant=None, **extra_data):
    payload = {
        'nm': name, 'pr': str(unit_price.amount), 'qt': quantity or 1}

    if item_id:
        payload['id'] = item_id
    if category:
        payload['ca'] = category
    if brand:
        payload['br'] = brand
    if variant:
        payload['va'] = variant

    payload.update(extra_data)
    return payload


def enhanced_purchase(
        transaction_id, items, revenue, url_page, tax=None, shipping=None,
        host=None, affiliation=None, coupon=None, **extra_data):
    if not items:
        raise ValueError('You need to specify at least one item')

    yield from event('ecommerce', 'purchase')

    payload = {
        'pa': 'purchase', 'ti': transaction_id, 'dp': url_page,
        'tr': str(revenue.amount), 'tt': '0'}
        
    if shipping:
        payload['ts'] = str(shipping)
    if tax is not None:
        payload['tt'] = str(tax.amount)
    if host:
        payload['dh'] = host
    if affiliation:
        payload['ta'] = self.affiliation
    if coupon:
        payload['tcc'] = coupon

    payload.update(extra_data)

    for position, item in enumerate(items):
        payload.update(_finalize_enhanced_purchase_item(item, position + 1))

    yield payload


def _finalize_enhanced_purchase_item(item, position):
    position_prefix = 'pr{0}'.format(position)
    final_item = {}
    for key, value in item.items():
        final_item[position_prefix + key] = value
    return final_item
