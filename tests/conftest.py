import pytest
from prices import Money


@pytest.fixture
def amount():
    return Money(10, currency='USD')