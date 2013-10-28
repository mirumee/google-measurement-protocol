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

```python
from google_measurement_protocol import PageView, report

view = PageView(path='/my-page/', title='My Page', referrer='http://example.com/')
report('UA-123456-1', client_id, view)
```


Reporting a transaction
-----------------------

```python
from google_measurement_protocol import Item, report, Transaction
from prices import Price

transaction_id = '0001'  # any string should do
items = [Item('My awesome product', Price(90, currency='EUR'), quantity=2),
         Item('Another product', Price(30, currency='EUR'))]
transaction = Transaction(transaction_id, items)
report('UA-123456-1', client_id, transaction)
```
