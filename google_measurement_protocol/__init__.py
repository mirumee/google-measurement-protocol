from collections import namedtuple

import requests

TRACKING_URI = 'https://ssl.google-analytics.com/collect'


def _make_request(data, headers):
    return requests.post(
        TRACKING_URI, data=data, headers=extra_headers, timeout=5.0)


def report(
        tracking_id, client_id, payloads, headers=None):
    """Actually report measurements to Google Analytics."""
    return [
        _make_request(data, headers) for data in finalize_payloads(
            tracking_id, client_id, requestable)]


def finalize_payloads(tracking_id, client_id, payloads):
    """Get final data for API requests for Google Analytics.

    Updates payloads setting required non-specific values on data.
    """
    extra_payload = {
        'v': '1', 'tid': tracking_id, 'cid': client_id, 'aip': '1'}

    for payload in payloads:
        final_payload = dict(payload)
        final_payload.update(extra_payload)
        yield final_payload


def pageview(
        path=None, host_name=None, location=None, title=None, language=None,
        referrer=None):
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
    return [payload]


def transaction(
        transaction_id, items, revenue, shipping=None, affiliation=None):
    payload = {'t': 'transaction', 'ti': self.transaction_id}
    if affiliation:
        payload['ta'] = affiliation
    payload['tr'] = str(revenue.gross.amount)
    payload['tt'] = str(revenue.tax.amount)
    payload['cu'] = revenue.currency
    
    if shipping:
        payload['ts'] = str(shipping.gross.amount)

    for item in items:
        item['ti'] = transaction_id

    return [payload] + items


def item(name, unit_price, quantity=None, item_id=None, category=None):
    payload = {
        't': 'item', 'in': name, 'ip': str(unit_price.gross.amount),
        'cu': unit_price.currency}
    if quantity:
        payload['iq'] = str(int(quantity))
    if item_id:
        payload['ic'] = item_id
    if category:
        payload['iv'] = category
    return payload


def event(category, action, label=None, value=None):
    payload = {'t': 'event', 'ec': category, 'ea': action}
    if label:
        payload['el'] = label
    if value:
        payload['ev'] = str(int(value))
    return [payload]


class EnhancedItem(namedtuple('EnhancedItem',
                   'name unit_price quantity item_id category brand variant')):

    def __new__(cls, name, unit_price, quantity=None, item_id=None,
                category=None, brand=None, variant=None):
        return super(EnhancedItem, cls).__new__(cls, name, unit_price,
                                                quantity, item_id, category,
                                                brand, variant)

    def get_subtotal(self):
        if self.quantity:
            return self.unit_price * self.quantity
        return self.unit_price

    def get_payload_for_transaction(self, position):
        payload = {
            'pr{0}ps'.format(position): '{0}'.format(position),
            'pr{0}nm'.format(position): self.name,
            'pr{0}pr'.format(position): self.unit_price}
        quantity = self.quantity or 1
        payload['pr{0}qt'.format(position)] = '{0}'.format(quantity)
        if self.item_id:
            payload['pr{0}id'.format(position)] = self.item_id
        if self.category:
            payload['pr{0}ca'.format(position)] = self.category
        if self.brand:
            payload['pr{0}br'.format(position)] = self.brand
        if self.variant:
            payload['pr{0}va'.format(position)] = self.variant

        return payload


class EnhancedPurchase(Requestable,
                       namedtuple('EnhancedPurchase', 'transaction_id items url_page revenue tax shipping host affiliation coupon')):

    def __new__(cls, transaction_id, items, url_page, revenue=None, tax=None,
                shipping=None, host=None, affiliation=None, coupon=None):
        if not items:
            raise ValueError('You need to specify at least one item')
        return super(EnhancedPurchase, cls).__new__(cls, transaction_id, items,
                                                    url_page, revenue, tax,
                                                    shipping, host,
                                                    affiliation, coupon)

    def get_total(self):
        if self.revenue:
            return self.revenue
        prices = [i.get_subtotal() for i in self.items]
        total = sum(prices[1:], prices[0])
        if self.shipping:
            total += self.shipping
        if self.tax:
            total += self.tax
        return total

    def get_payload(self):
        payload = {
            'pa': 'purchase',
            'ti': self.transaction_id,
            'dp': self.url_page}
        tax = self.tax or 0
        payload['tt'] = str(tax)
        total = self.get_total()
        payload['tr'] = '{0}'.format(total)
        if self.shipping:
            payload['ts'] = str(self.shipping)
        if self.host:
            payload['dh'] = self.host
        if self.affiliation:
            payload['ta'] = self.affiliation
        if self.coupon:
            payload['tcc'] = self.coupon
        return payload

    def __iter__(self):
        event = Event('ecommerce', 'purchase')
        yield event.get_payload()
        to_return = self.get_payload()
        for i in range(len(self.items)):
            to_return.update(self.items[i].get_payload_for_transaction(i + 1))
        yield to_return
