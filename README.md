google-measurement-protocol
===========================

A Python implementation of Google Analytics Measurement Protocol

Transaction handling depends on the `prices` library.


Generating a client ID
----------------------

Google strongly encourages using UUID version 4 as unique user handles.
It's up to you to generate and persist the ID between actions, just make
sure that all actions performed by the same user are reported using the
same client ID.

```python
import uuid

client_id = uuid.uuid4()
```


Reporting a page view
---------------------

There are two ways to obtain a page view data to send to Google Analytics:
```python
pageview(path[, host_name=None][, title=None][, language=None][, referrer=None])
```
```python
pageview(location='http://example.com/my-page/?foo=1'[, title=None][, language=None][, referrer=None])
```

Example:
```python
from google_measurement_protocol import pageview, report

data = pageview(path='/my-page/', title='My Page', referrer='http://example.com/')
report('UA-123456-1', client_id, data)
```


Reporting an event
------------------

Use the `event` function to obtain data:
```python
event('category', 'action'[, label=None][, value=None])
```

Example:
```python
from google_measurement_protocol import event, report

data = event('profile', 'user_registered')
report('UA-123456-1', client_id, data)
```


Reporting a transaction
-----------------------

First create `Item`s to describe the contents of the transaction:
```python
item(name, unit_price[, quantity=None][, item_id=None][, category=None])
```

Then the `transaction` itself:
```python
transaction(transaction_id, items, revenue[, tax=None][, shipping=None][, affiliation=None])
```

Example:
```python
from google_measurement_protocol import item, report, transaction
from prices import Money

transaction_id = '0001'  # any string should do
items = [
    item('My awesome product', Money(10, 'EUR'), quantity=2),
    item('Another product', Money(17, 'EUR'))]
data = transaction(transaction_id, items, Money(37, 'EUR'))
report('UA-123456-1', client_id, data)
```


Reporting an extended ecommerce purchase
----------------------------------------

For Extended Ecommerce we have implemented Purchase tracking, please note
this will add an event automatically, as required by Google Analytics.

First use `enhanced_item`s to describe the contents of the transaction:
```python
enhanced_item(
    name, unit_price[, quantity=None][, item_id=None][, category=None]
    [, brand=None][, variant=None])
```

Then the `enhanced_purchase` itself:
```python
enhanced_purchase(
    transaction_id, items, revenue, url_page[, tax=None][, shipping=None]
    [, host=None][, affiliation=None])
```
Please note you have to add an explicit path
when creating your `enhanced_purchase` instance.

Example:
```python
from google_measurement_protocol import enhanced_item, enhanced_purchase, report

transaction_id = '0001'  # any string should do
items = [
    enhanced_item('My awesome product', Money(10, 'USD'), quantity=2),
    enhanced_item('Another product', Money(15, 'USD'))]
data = enhanced_purchase(transaction_id, items, Money(27, 'USD'), '/cart/')
report('UA-123456-1', client_id, data)
```


Reporting extra data
--------------------

In adition to documented arguments, all functions accept any number of extra named arguments, that are then in the data.

For example. to include language parameter in sent `event`, you may do this:
```python
from google_measurement_protocol import event, report

data = event('profile', 'user_registered', ul='en-us')
report('UA-123456-1', client_id, data)
```

`report` also supports passing extra data, which is then added to every payload sent to API. This example is equal to previous one:

```python
from google_measurement_protocol import event, report

data = event('profile', 'user_registered')
report('UA-123456-1', client_id, data, ul='en-us')
```

You can also pass `extra_headers` to `report()` function to submit
additional information. It is passed directly as additional headers to
`requests` library. This is currently the only way to pass `User-Agent`.

Example:
```python
from google_measurement_protocol import PageView, report, SystemInfo

data = pageview(path='/my-page/', title='My Page', referrer='http://example.com/')
headers = {'user-agent': 'my-user-agent 1.0'}
report('UA-123456-1', client_id, data, extra_header=headers)
```