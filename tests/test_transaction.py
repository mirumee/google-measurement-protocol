import pytest
from prices import Money

from google_measurement_protocol import item, transaction


@pytest.fixture
def single_item_list():
    return [item('item-01', Money(10, 'USD'))]


def test_no_items():
    generator = transaction('trans-01', [], Money(0, 'USD'))
    with pytest.raises(ValueError):
        list(generator)


def test_required_params(single_item_list):
    generator = transaction('trans-01', single_item_list, Money(10, 'USD'))
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'tt': '0'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_tax(single_item_list):
    generator = transaction(
        'trans-01', single_item_list, Money(10, 'USD'), tax=Money(2, 'USD'))
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'tt': '2'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_shipping(single_item_list):
    generator = transaction(
        'trans-01', single_item_list, Money(10, 'USD'),
        shipping=Money(100, currency='USD'))
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'cu': 'USD', 'tr': '10',
            'ts': '100', 'tt': '0'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_affiliation(single_item_list):
    generator = transaction(
        'trans-01', single_item_list, Money(10, 'USD'), affiliation='loyalty')
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'tr': '10', 'tt': '0',
            'cu': 'USD', 'ta': 'loyalty'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]


def test_extra_params(single_item_list):
    generator = transaction(
        'trans-01', single_item_list, Money(10, 'USD'), ex='extra')
    assert list(generator) == [
        {
            't': 'transaction', 'ti': 'trans-01', 'tr': '10', 'tt': '0',
            'cu': 'USD', 'ex': 'extra'},
        {
            't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD',
            'ti': 'trans-01'}]
