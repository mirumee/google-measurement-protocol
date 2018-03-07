import pytest

from google_measurement_protocol import enhanced_item, enhanced_purchase, event


def test_no_items(price):
    generator = enhanced_purchase('trans-01', [], price, '/cart/')
    with pytest.raises(ValueError):
        list(generator)


def test_required_params(price):
    items = [enhanced_item('item-01', price)]
    generator = enhanced_purchase('trans-01', items, price, '/cart/')
    assert list(generator) == [
        {'t': 'event', 'ec': 'ecommerce', 'ea': 'purchase'},
        {
            'pa': 'purchase', 'ti': 'trans-01', 'dp': '/cart/', 'tt': '0',
            'tr': '10', 'pr1nm': 'item-01', 'pr1pr': '10', 'pr1qt': 1}]


def test_coupon(price):
    items = [enhanced_item('item-01', price)]
    generator = enhanced_purchase(
        'trans-01', items, price, '/cart/', coupon='TESTCOUPON')
    assert list(generator) == [
        {'t': 'event', 'ec': 'ecommerce', 'ea': 'purchase'},
        {
            'pa': 'purchase', 'ti': 'trans-01', 'dp': '/cart/', 'tt': '0',
            'tr': '10', 'tcc': 'TESTCOUPON', 'pr1nm': 'item-01', 'pr1pr': '10',
            'pr1qt': 1}]


def test_extra_params(price):
    items = [enhanced_item('item-01', price)]
    generator = enhanced_purchase(
        'trans-01', items, price, '/cart/', ex='extra')
    assert list(generator) == [
        {'t': 'event', 'ec': 'ecommerce', 'ea': 'purchase'},
        {
            'pa': 'purchase', 'ti': 'trans-01', 'dp': '/cart/', 'tt': '0',
            'tr': '10', 'ex': 'extra', 'pr1nm': 'item-01', 'pr1pr': '10',
            'pr1qt': 1}]