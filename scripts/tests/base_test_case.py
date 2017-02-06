import unittest
import difflib


class BaseTestCase(unittest.TestCase):
    """Base class for tests, providing some basic services."""

    def assertTextEqual(self, t1, t2):
        """Checks if two texts are the same. If not, prints a diff."""
        if t1 != t2:
            diff = difflib.ndiff(t1.splitlines(True),
                                 t2.splitlines(True))
            print("".join(diff))
            self.fail("expected output and obtained output are different")
