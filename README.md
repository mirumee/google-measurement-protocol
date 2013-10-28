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

There are two ways to construct a `PageView` object:
```python
PageView('/my-page/'[, host_name=None][, title=None][, referrer=None])
```
```python
PageView(location='http://example.com/my-page/?foo=1'[, title=None][, referrer=None])
```

Example:
```python
from google_measurement_protocol import PageView, report

view = PageView(path='/my-page/', title='My Page', referrer='http://example.com/')
report('UA-123456-1', client_id, view)
```


Reporting an event
------------------

Use the `Event` object:
```python
Event('category', 'action'[, label=None][, value=None])
```

Example:
```python
from google_measurement_protocol import Event, report

event = Event('profile', 'user_registered')
report('UA-123456-1', client_id, event)
```


Reporting a transaction
-----------------------

First create `Item`s to describe the contents of the transaction:
```python
Item('product name', unit_price=Price(10, currency='EUR')[, quantity=None][, item_id=None])
```

Then the `Transaction` itself:
```python
Transaction('transaction id', items[, revenue=None][, shipping=None][, affiliation=None])
```
If `revenue` is given, it will override the total that is otherwise calculated from items and shipping.

Example:
```python
from google_measurement_protocol import Item, report, Transaction
from prices import Price

transaction_id = '0001'  # any string should do
items = [Item('My awesome product', Price(90, currency='EUR'), quantity=2),
         Item('Another product', Price(30, currency='EUR'))]
transaction = Transaction(transaction_id, items)
report('UA-123456-1', client_id, transaction)
```
