import time
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import *
from requests.packages.urllib3.util.retry import Retry


class Reretry(Retry):

	def __init__(self, **kwargs):
		self.__callbacks = kwargs.pop("callbacks", {})
		super(Reretry, self).__init__(**kwargs)

	def new(self, **kwargs):
		kwargs["callbacks"] = self.__callbacks
		return super(Reretry, self).new(**kwargs)

	def increment(self, method, url, *args, **kwargs):
		if self.__callbacks.get("retry", None):
			self.__callbacks["retry"](url)
		return super(Reretry, self).increment(method, url, *args, **kwargs)

	def sleep(self, *args,  **kwargs):
		if self.__callbacks.get("sleep", None):
			t0 = time.time()
			r = super(Reretry, self).sleep(*args, **kwargs)
			self.__callbacks["sleep"](time.time() - t0)
			return r
		return super(Reretry, self).sleep(*args, **kwargs)


class Request(object):

	def __init__(self, retries=3, backoff_factor=0.3, 
			status_forcelist=(500, 501, 502, 503, 504), 
			session=None, timeout=None, cert=None, callbacks={}):

		self.retries = 3
		self.backoff_factor = 0.3
		self.status_forcelist = status_forcelist
		self.session = session or requests.Session()
		self.timeout = timeout
		self.cert = cert
		self.callbacks = callbacks

		retry = Reretry(
			total=retries,
			read=retries,
			connect=retries,
			backoff_factor=backoff_factor,
			status_forcelist=status_forcelist,
			callbacks=callbacks,
		)
		a = HTTPAdapter(max_retries=retry)
		self.session.mount("http://", a)
		self.session.mount("https://", a)


	def do(self, method, url, **kwargs):

		timeout = kwargs.pop("timeout", None) or self.timeout
		cert = kwargs.pop("cert", None) or self.cert

		if self.callbacks.get("pre_request", None):
			self.callbacks["pre_request"](url)

		r = self.session.request(method, url,
			timeout=timeout, cert=cert, **kwargs)
	
		if self.callbacks.get("post_request", None):
			self.callbacks["post_request"](url)

		return r


if __name__ == "__main__":
	#try:
	#	r = request_retry().get("http://127.0.0.1:6666/badservice/status/500")
	#except Exception as e:
	#	print(repr(e))
	#
	#print(r.text)

	def cb(url):
		print("call from retry URL:", url)

	def cb2(duration):
		print("Call from sleep. Slept for", duration)

	def cb3(url):
		print("Call from pre_request", url)

	def cb4(url):
		print("Call from post_request", url)

	#req = Request(timeout=2, callbacks={"retry":cb, "sleep": cb2, "pre_request":cb3, "post_request":cb4})
	#req = Request(timeout=2, callbacks={})
	req = Request(timeout=2)

	urls = [
		"http://127.0.0.1:6666/badservice/status/200",
		"http://127.0.0.1:6666/badservice/status/400",
		"http://127.0.0.1:6666/badservice/status/503",
		"http://127.0.0.1:6666/badservice/drop",
		"http://127.0.0.1:6666/badservice/delay/10000",
	]

	for u in urls:
		t0 = time.time()
		try:
			res = req.do("GET", u)
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



