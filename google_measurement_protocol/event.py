def event(category, action, label=None, value=None, **extra_info):
    payload = {'t': 'event', 'ec': category, 'ea': action}
    if label:
        payload['el'] = label
    if value:
        payload['ev'] = str(int(value))
    payload.update(extra_info)
    return payload