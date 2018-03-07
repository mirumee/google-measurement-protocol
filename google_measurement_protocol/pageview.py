def pageview(
        path=None, host_name=None, location=None, title=None, language=None,
        referrer=None, **extra_data):
    payload = {'t': 'pageview'}

    if location:
        payload['dl'] = location
    if host_name:
        payload['dh'] = host_name
    if path:
        payload['dp'] = path
    if title:
        payload['dt'] = title
    if referrer:
        payload['dr'] = referrer
    if language:
        payload['ul'] = language

    payload.update(extra_data)
    yield payload