import unittest
from pr_1.main import find_quadratic_roots, errInvalidArg, errInvalidCf, errNoRoots


class TestPr1(unittest.TestCase):
    def test_success_test(self):
        res = find_quadratic_roots(1, -3, 2)
        self.assertEqual(res, (2.0, 1.0))

    def test_invalid_argument(self):
        with self.assertRaises(ValueError) as context:
            find_quadratic_roots(0, -3, 2)
        self.assertEqual(str(context.exception), errInvalidArg)

    def test_invalid_cf(self):
        with self.assertRaises(ValueError) as context:
            find_quadratic_roots(1, "tri", 2)
        self.assertEqual(str(context.exception), errInvalidCf)

    def test_error_no_roots(self):
        with self.assertRaises(ValueError) as context:
            find_quadratic_roots(2, -3, 2)
        self.assertEqual(str(context.exception), errNoRoots)
