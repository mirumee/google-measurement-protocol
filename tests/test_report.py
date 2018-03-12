from urllib.parse import parse_qs

from httmock import response, urlmatch, with_httmock

from google_measurement_protocol import report


@urlmatch(netloc=r'ssl\.google-analytics\.com', path='/collect')
def ga_mock(url, request):
    qs = parse_qs(request.body)
    return response(200, qs)


@with_httmock(ga_mock)
def test_report():
    (response,) = report('UA-123456-78', 'CID', [{'t': 'mock'}])
    data = response.json()
    assert data == {
        'cid': ['CID'], 'tid': ['UA-123456-78'], 'v': ['1'], 'aip': ['1'],
        't': ['mock']}


@with_httmock(ga_mock)
def test_extra_params():
    (response,) = report('UA-123456-78', 'CID', [{'t': 'mock'}], ex='extra')
    data = response.json()
    assert data['ex'] == ['extra']
