
# rerequest

Python `requests` replacement module with retries for timeout, dropped connections and status codes.

## Default values (constructor)

```python
class Request(object):

    def __init__(self, retries=3, backoff_factor=0.3,
            status_forcelist=(500, 501, 502, 503, 504),
            session=None, timeout=None, cert=None, callbacks={}):
```

## Simple usage with default values

```python
from rerequest import DefaultRequest as requests

res = requests.get("http://google.com")
print(res)
```
## Usage with custom values

```python
from rerequest import Request

rq = Request(timeout=10)
res = rq.get("http://google.com")
print(res)
```
## Callback functions

```python
from rerequest import Request

def cb(url):
    print("call from retry URL:", url)

def cb2(duration):
    print("Call from sleep. Slept for", duration)

def cb3(url):
    print("Call from pre_request", url)

def cb4(url):
    print("Call from post_request", url)


callbacks={"retry":cb, "sleep": cb2, "pre_request":cb3, "post_request":cb4}

rq = Request(callbacks=callbacks)
res = rq.get("http://google.com")
print(res)

```

## Tests
On your virtual environment:
1. `pip install coverage`
2. Make sure [badservice](https://github.com/diegohce/badservice/releases/download/v0.1.0/badservice-0.1.0-linux_x64.tar.bz2) is running on `127.0.0.1:6666`
3.  `coverage run -m tests.all_test.py`
4.  `coverage report -m rerequest/__init__.py`
