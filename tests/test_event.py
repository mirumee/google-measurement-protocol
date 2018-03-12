from prices import Money, TaxedMoney

from google_measurement_protocol import event


def test_required_params():
    generator = event('category', 'action')
    assert list(generator) == [{'t': 'event', 'ec': 'category', 'ea': 'action'}]


def test_optional_params():
    generator = event('category', 'action', label='label', value=7)
    assert list(generator) == [
        {
            't': 'event', 'ec': 'category', 'ea': 'action', 'el': 'label',
            'ev': '7'}]


def test_extra_params():
    generator = event('category', 'action', ex='extra')
    assert list(generator) == [
        {'t': 'event', 'ec': 'category', 'ea': 'action', 'ex': 'extra'}]
