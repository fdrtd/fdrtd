import unittest as _unittest


class TestAssertions(_unittest.TestCase):

    def outer_assertion(self, res1, res2, msg):
        if isinstance(res1, tuple):
            for x, y in zip(res1, res2):
                self.outer_assertion(x, y, msg)
        elif isinstance(res1, list):
            for x, y in zip(sorted(res1), sorted(res2)):
                self.outer_assertion(x, y, msg)
        elif isinstance(res1, dict):
            for key in res1:
                self.outer_assertion(res1[key], res2[key], msg)
        else:
            self.inner_assertion(res1, res2, msg)

    def inner_assertion(self, x, y, msg):
        if isinstance(x, float):
            self.assertAlmostEqual(first=x, second=y, places=4, msg=msg)
        else:
            self.assertEqual(first=x, second=y, msg=msg)
