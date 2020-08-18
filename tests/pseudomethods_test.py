#encoding: utf-8

import unittest
from rerequest import DefaultRequest as requests


class PseudomethodsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get(self):
        res = requests.get("http://127.0.0.1:6666/badservice/status/200")
        self.assertEqual(res.status_code, 200)

    def test_post(self):
        res = requests.post("http://127.0.0.1:6666/badservice/status/200", json={"name":"diego"})

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.content) > 0)
        self.assertEqual(res.json()["name"], "diego")

    def test_put(self):
        res = requests.put("http://127.0.0.1:6666/badservice/status/200")
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        res = requests.delete("http://127.0.0.1:6666/badservice/status/200")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()

