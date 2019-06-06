import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import *
from requests.packages.urllib3.util.retry import Retry


def request_retry(retries=3, backoff_factor=0.3,
		status_forcelist=(500, 502, 503, 504), session=None):

	s = session or requests.Session()

	retry = Retry(
		total=retries,
		read=retries,
		connect=retries,
		backoff_factor=backoff_factor,
		status_forcelist=status_forcelist,
	)
	a = HTTPAdapter(max_retries=retry)
	s.mount("http://", a)
	s.mount("https://", a)

	return s


class Request(object):

	def __init__(self, retries=3, backoff_factor=0.3, 
			status_forcelist=(500, 502, 503, 504), 
			session=None, timeout=None, cert=None):

		self.retries = 3
		self.backoff_factor = 0.3
		self.status_forcelist = status_forcelist
		self.session = session or requests.Session()
		self.timeout = timeout
		self.cert = cert

		retry = Retry(
			total=retries,
			read=retries,
			connect=retries,
			backoff_factor=backoff_factor,
			status_forcelist=status_forcelist,
		)
		a = HTTPAdapter(max_retries=retry)
		self.session.mount("http://", a)
		self.session.mount("https://", a)


	def do(self, method, url, **kwargs):

		r = self.session.request(method, url,
			timeout=self.timeout, cert=self.cert, **kwargs)
	
		return r


if __name__ == "__main__":
	#try:
	#	r = request_retry().get("http://127.0.0.1:6666/badservice/status/500")
	#except Exception as e:
	#	print(repr(e))
	#
	#print(r.text)



	req = Request(timeout=0.1)

	urls = [
		"http://127.0.0.1:6666/badservice/status/200",
		"http://127.0.0.1:6666/badservice/status/400",
		"http://127.0.0.1:6666/badservice/status/503",
		"http://127.0.0.1:6666/badservice/drop",
		"http://127.0.0.1:6666/badservice/delay/10000",
	]

	for u in urls:
		try:
			res = req.do("GET", u)
		except RetryError as e:
			print("RetryError", repr(e) )
			print()

		except ConnectionError as e:
			print("ConnectionError", repr(e) )
			print()

		except RequestException as e:
			print ("RequestException", repr(e) )
			print()

		except Exception as e:
			print("Exception", repr(e) )
			print()

		else:
			print("status:", res.status_code)



