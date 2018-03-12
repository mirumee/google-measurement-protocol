from google_measurement_protocol import pageview


def test_by_path():
    pv1_generator = pageview('/my-page/')
    assert list(pv1_generator) == [{'t': 'pageview', 'dp': '/my-page/'}]

    pv2_generator = pageview('/my-page/', host_name='example.com')
    assert list(pv2_generator) == [
        {'t': 'pageview', 'dp': '/my-page/', 'dh': 'example.com'}]


def test_by_location():
    generator = pageview(location='http://example.com/my-page/')
    assert list(generator) == [
        {'t': 'pageview', 'dl': 'http://example.com/my-page/'}]


def test_optional_params():
    generator = pageview('/', title='title', referrer='referrer')
    assert list(generator) == [
        {'t': 'pageview', 'dp': '/', 'dr': 'referrer', 'dt': 'title'}]


def test_extra_params():
    generator = pageview('/my-page/', ex='extra')
    assert list(generator) == [
        {'t': 'pageview', 'dp': '/my-page/', 'ex': 'extra'}]
