from google_measurement_protocol import item


def test_required_params(price):
    data = item('item-01', price)
    assert data == {'t': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD'}


def test_quantity(price):
    data = item('item-01', price, quantity=2)
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'iq': '2'}


def test_optional_params(price):
    data = item('item-01', price, item_id='it01', category='cat')
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'ic': 'it01',
        'iv': 'cat'}


def test_extra_params(price):
    data = item('item-01', price, ex='extra')
    assert data == {
        't': 'item', 'in': 'item-01', 'ip': '10', 'cu': 'USD', 'ex': 'extra'}
