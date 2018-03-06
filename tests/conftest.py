import pytest
from prices import Money, TaxedMoney


@pytest.fixture
def price():
    return TaxedMoney(
        net=Money(8, currency='USD'), gross=Money(10, currency='USD'))