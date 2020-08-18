#encoding: utf-8

import time
import unittest
from rerequest import (
    Request, 
    RetryError,
    RequestException,
)


def cb(url):
    print("call from retry URL:", url)

def cb2(duration):
    print("Call from sleep. Slept for", duration)

def cb3(url):
    print("Call from pre_request", url)

def cb4(url):
    print("Call from post_request", url)



class ExceptionsTestWithCallbacks(unittest.TestCase):

    def setUp(self):
        self.req = Request(timeout=2, callbacks={"retry":cb, "sleep": cb2, "pre_request":cb3, "post_request":cb4})

        self.urls = [
            "http://127.0.0.1:6666/badservice/status/200",
            "http://127.0.0.1:6666/badservice/status/400",
            "http://127.0.0.1:6666/badservice/status/503",
            "http://127.0.0.1:6666/badservice/drop",
            "http://127.0.0.1:6666/badservice/delay/10000",
        ]

    def test_Exceptions(self): 
        for u in self.urls:
            t0 = time.time()
            try:
                res = self.req.do("GET", u)
            except RetryError as e:
                t1 = time.time() - t0
                print("RetryError", t1, repr(e) )
                print()

            except ConnectionError as e:
                t1 = time.time() - t0
                print("ConnectionError", t1, repr(e) )
                print()

            except RequestException as e:
                t1 = time.time() - t0
                print ("RequestException", t1, repr(e) )
                print()

            except Exception as e:
                t1 = time.time() - t0
                print("Exception", t1, repr(e) )
                print()

            else:
                t1 = time.time() - t0
                print("status:", t1, res.status_code)

class ExceptionsTest(unittest.TestCase):

    def setUp(self):
        self.req = Request(timeout=2)

        self.urls = [
            "http://127.0.0.1:6666/badservice/status/200",
            "http://127.0.0.1:6666/badservice/status/400",
            "http://127.0.0.1:6666/badservice/status/503",
            "http://127.0.0.1:6666/badservice/drop",
            "http://127.0.0.1:6666/badservice/delay/10000",
        ]

    def test_Exceptions(self): 
        for u in self.urls:
            t0 = time.time()
            try:
                res = self.req.do("GET", u)
            except RetryError as e:
                t1 = time.time() - t0
                print("RetryError", t1, repr(e) )
                print()

            except ConnectionError as e:
                t1 = time.time() - t0
                print("ConnectionError", t1, repr(e) )
                print()

            except RequestException as e:
                t1 = time.time() - t0
                print ("RequestException", t1, repr(e) )
                print()

            except Exception as e:
                t1 = time.time() - t0
                print("Exception", t1, repr(e) )
                print()

            else:
                t1 = time.time() - t0
                print("status:", t1, res.status_code)

if __name__ == "__main__":
    unittest.main()

