from collections import namedtuple

import requests

TRACKING_URI = 'https://ssl.google-analytics.com/collect'


def _request(data, extra_headers):
    return requests.post(TRACKING_URI, data=data, headers=extra_headers,
                         timeout=5.0)


def report(tracking_id, client_id, requestable, extra_info=None,
           extra_headers=None):
    """Actually report measurements to Google Analytics."""
    return [_request(data, extra_headers)
            for data, extra_headers in payloads(
            tracking_id, client_id, requestable, extra_info, extra_headers)]


def payloads(tracking_id, client_id, requestable, extra_info=None,
             extra_headers=None):
    """Get data and headers of API requests for Google Analytics.

    Generates a sequence of (data, headers) pairs. Both `data` and `headers`
    are dicts.
    """
    extra_payload = {
        'v': '1',
        'tid': tracking_id,
        'cid': client_id,
        'aip': '1'}
    if extra_info:
        for payload in extra_info:
            extra_payload.update(payload)

    for request_payload in requestable:
        final_payload = dict(request_payload)
        final_payload.update(extra_payload)
        yield final_payload, extra_headers


class Requestable(object):

    def get_payload(self):
        raise NotImplementedError()

    def __iter__(self):
        yield self.get_payload()


class SystemInfo(Requestable, namedtuple('SystemInfo', 'language')):

    def __new__(cls, language=None):
        return super(SystemInfo, cls).__new__(cls, language)

    def get_payload(self):
        payload = {}
        if self.language:
            payload['ul'] = self.language
        return payload


class PageView(
        Requestable,
        namedtuple('PageView',
                   'path host_name location title referrer')):

    def __new__(cls, path=None, host_name=None, location=None, title=None,
                referrer=None):
        return super(PageView, cls).__new__(cls, path, host_name, location,
                                            title, referrer)

    def get_payload(self):
        payload = {'t': 'pageview'}
        if self.location:
            payload['dl'] = self.location
        if self.host_name:
            payload['dh'] = self.host_name
        if self.path:
            payload['dp'] = self.path
        if self.title:
            payload['dt'] = self.title
        if self.referrer:
            payload['dr'] = self.referrer
        return payload


class Event(Requestable, namedtuple('Event', 'category action label value')):

    def __new__(cls, category, action, label=None, value=None):
        return super(Event, cls).__new__(cls, category, action, label, value)

    def get_payload(self):
        payload = {
            't': 'event',
            'ec': self.category,
            'ea': self.action}
        if self.label:
            payload['el'] = self.label
        if self.value:
            payload['ev'] = str(int(self.value))
        return payload


class Transaction(
        Requestable,
        namedtuple('Transaction',
                   'transaction_id items revenue shipping affiliation')):

    def __new__(cls, transaction_id, items, revenue=None, shipping=None,
                affiliation=None):
        if not items:
            raise ValueError('You need to specify at least one item')
        return super(Transaction, cls).__new__(
            cls, transaction_id, items, revenue, shipping, affiliation)

    def get_total(self):
        if self.revenue:
            return self.revenue
        prices = [i.get_subtotal() for i in self.items]
        total = sum(prices[1:], prices[0])
        if self.shipping:
            total += self.shipping
        return total

    def get_payload(self):
        payload = {
            't': 'transaction',
            'ti': self.transaction_id}
        if self.affiliation:
            payload['ta'] = self.affiliation
        total = self.get_total()
        payload['tr'] = str(total.gross)
        payload['tt'] = str(total.tax)
        payload['cu'] = total.currency
        if self.shipping:
            payload['ts'] = str(self.shipping.gross)
        return payload

    def __iter__(self):
        yield self.get_payload()
        for i in self.items:
            yield i.get_payload_for_transaction(self.transaction_id)


class Item(namedtuple('Item', 'name unit_price quantity item_id category')):

    def __new__(cls, name, unit_price, quantity=None, item_id=None,
                category=None):
        return super(Item, cls).__new__(cls, name, unit_price, quantity,
                                        item_id, category)

    def get_subtotal(self):
        if self.quantity:
            return self.unit_price * self.quantity
        return self.unit_price

    def get_payload_for_transaction(self, transaction_id):
        payload = {
            't': 'item',
            'ti': transaction_id,
            'in': self.name}
        payload['ip'] = str(self.unit_price.gross)
        payload['cu'] = self.unit_price.currency
        if self.quantity:
            payload['iq'] = str(int(self.quantity))
        if self.item_id:
            payload['ic'] = self.item_id
        if self.category:
            payload['iv'] = self.category
        return payload


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
