from prices import Money

from google_measurement_protocol import item


def test_required_params():
    data = item('item-01', Money(10, 'USD'))
    assert data == {'t': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD'}


def test_quantity():
    data = item('item-01', Money(10, 'USD'), quantity=2)
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'iq': '2'}


def test_optional_params():
    data = item('item-01', Money(10, 'USD'), item_id='it01', category='cat')
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'ic': 'it01',
        'iv': 'cat'}


def test_extra_params():
    data = item('item-01', Money(10, 'USD'), ex='extra')
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'ex': 'extra'}