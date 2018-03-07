from google_measurement_protocol import item


def test_required_params(amount):
    data = item('item-01', amount)
    assert data == {'t': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD'}


def test_quantity(amount):
    data = item('item-01', amount, quantity=2)
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'iq': '2'}


def test_optional_params(amount):
    data = item('item-01', amount, item_id='it01', category='cat')
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'ic': 'it01',
        'iv': 'cat'}


def test_extra_params(amount):
    data = item('item-01', amount, ex='extra')
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'ex': 'extra'}