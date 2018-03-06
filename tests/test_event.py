from urllib.parse import parse_qs

from prices import Money, TaxedMoney

from google_measurement_protocol import event


def test_required_params():
    data = event('category', 'action')
    assert data == {'t': 'event', 'ec': 'category', 'ea': 'action'}


def test_optional_params():
    data = event('category', 'action', label='label', value=7)
    assert data == {
        't': 'event', 'ec': 'category', 'ea': 'action', 'el': 'label',
        'ev': '7'}


def test_extra_params():
    data = event('category', 'action', ex='extra')
    assert data == {
        't': 'event', 'ec': 'category', 'ea': 'action', 'ex': 'extra'}
