#encoding: utf-8

import unittest

from tests.pseudomethods_test import (
    PseudomethodsTest,
)

from tests.exceptions_test import (
    ExceptionsTest,
    ExceptionsTestWithCallbacks,
)

tests = (
    PseudomethodsTest(),
    ExceptionsTest(),
    ExceptionsTestWithCallbacks(),
)

suite = unittest.TestSuite(tests=tests)


if __name__ == "__main__":
    unittest.main()

