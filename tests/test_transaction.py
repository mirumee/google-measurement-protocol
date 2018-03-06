import pytest
from prices import Money, TaxedMoney

from google_measurement_protocol import item, transaction


@pytest.fixture
def single_item_list(price):
    return [item('item-01', price)]


def test_no_items(price):
    generator = transaction('trans-01', [], price)
    with pytest.raises(ValueError):
        list(generator)


def test_required_params(price, single_item_list):
    generator = transaction('trans-01', single_item_list, price)
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'tt': '2'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_shipping(price, single_item_list):
    shipping_price = TaxedMoney(
        net=Money(95, currency='USD'), gross=Money(100, currency='USD'))

    generator = transaction(
        'trans-01', single_item_list, price, shipping=shipping_price)
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'ts': '100', 'tt': '2'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_affiliation(price, single_item_list):
    generator = transaction(
        'trans-01', single_item_list, price, affiliation='loyalty')
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'tr': '10', 'tt': '2',
            'cu': 'USD', 'ta': 'loyalty'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_extra_params(price, single_item_list):
    generator = transaction(
        'trans-01', single_item_list, price, ex='extra')
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'tr': '10', 'tt': '2',
            'cu': 'USD', 'ex': 'extra'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]
