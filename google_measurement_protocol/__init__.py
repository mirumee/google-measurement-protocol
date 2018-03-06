from collections import namedtuple

import requests

TRACKING_URI = 'https://ssl.google-analytics.com/collect'


def _make_request(data, headers):
    return requests.post(
        TRACKING_URI, data=data, headers=extra_headers, timeout=5.0)


def report(
        tracking_id, client_id, payloads, headers=None, **extra_info):
    """Actually report measurements to Google Analytics."""
    return [
        _make_request(data, headers) for data in finalize_payloads(
            tracking_id, client_id, requestable, **extra_info)]


def finalize_payloads(tracking_id, client_id, payloads, **extra_info):
    """Get final data for API requests for Google Analytics.

    Updates payloads setting required non-specific values on data.
    """
    extra_payload = {
        'v': '1', 'tid': tracking_id, 'cid': client_id, 'aip': '1'}

    for payload in payloads:
        final_payload = dict(payload)
        final_payload.update(extra_payload)
        final_payload.update(extra_info)
        yield final_payload


def pageview(
        path=None, host_name=None, location=None, title=None, language=None,
        referrer=None, **extra_info):
    payload = {'t': 'pageview'}

    if location:
        payload['dl'] = location
    if host_name:
        payload['dh'] = host_name
    if path:
        payload['dp'] = path
    if title:
        payload['dt'] = title
    if referrer:
        payload['dr'] = referrer
    if language:
        payload['ul'] = language

    payload.update(extra_info)
    yield payload


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


def event(category, action, label=None, value=None, **extra_info):
    payload = {'t': 'event', 'ec': category, 'ea': action}
    if label:
        payload['el'] = label
    if value:
        payload['ev'] = str(int(value))
    payload.update(extra_info)
    return payload


def enhanced_item(
        name, unit_price, quantity=None, item_id=None, category=None,
        brand=None, variant=None, **extra_info):
    payload = {'nm': name, 'pr': unit_price, 'qt': quantity or 1}

    if item_id:
        payload['id'] = item_id
    if category:
        payload['ca'] = category
    if brand:
        payload['br'] = brand
    if variant:
        payload['va'] = variant

    payload.update(extra_info)
    return payload


def enhanced_purchase(
        transaction_id, items, url_page, revenue, tax=None, shipping=None,
        host=None, affiliation=None, coupon=None, **extra_info):
    if not items:
        raise ValueError('You need to specify at least one item')

    yield event('ecommerce', 'purchase')

    payload = {
        'pa': 'purchase', 'ti': transaction_id, 'dp': url_page,
        'tt': str(tax or 0), 'tr': str(revenue)}
        
    if shipping:
        payload['ts'] = str(shipping)
    if host:
        payload['dh'] = host
    if affiliation:
        payload['ta'] = self.affiliation
    if coupon:
        payload['tcc'] = coupon

    payload.update(extra_info)

    for position, item in enumerate(items):
        payload.update(finalize_enhanced_purchase_item(item, position + 1))

    yield payload


def finalize_enhanced_purchase_item(item, position):
    position_prefix = 'pr{0}'.format(position)
    final_item = {}
    for key, value in item.items():
        final_item[position_prefix + key] = value
    return final_item
