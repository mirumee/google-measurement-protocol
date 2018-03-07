import pytest
from prices import Money

from google_measurement_protocol import item, transaction


@pytest.fixture
def single_item_list(amount):
    return [item('item-01', amount)]


def test_no_items(amount):
    generator = transaction('trans-01', [], amount)
    with pytest.raises(ValueError):
        list(generator)


def test_required_params(amount, single_item_list):
    generator = transaction('trans-01', single_item_list, amount)
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'tt': '0'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_tax(amount, single_item_list):
    tax = Money(2, currency='USD')
    generator = transaction('trans-01', single_item_list, amount, tax=tax)
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'tt': '2'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_shipping(amount, single_item_list):
    shipping_price = Money(100, currency='USD')
    generator = transaction(
        'trans-01', single_item_list, amount, shipping=shipping_price)
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'ts': '100', 'tt': '0'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_affiliation(amount, single_item_list):
    generator = transaction(
        'trans-01', single_item_list, amount, affiliation='loyalty')
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'tr': '10', 'tt': '0',
            'cu': 'USD', 'ta': 'loyalty'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_extra_params(amount, single_item_list):
    generator = transaction(
        'trans-01', single_item_list, amount, ex='extra')
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'tr': '10', 'tt': '0',
            'cu': 'USD', 'ex': 'extra'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]