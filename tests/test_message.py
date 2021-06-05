import unittest

import client
import server


class TestMessage(unittest.TestCase):
    """test class of keisan.py
    """

    def test_tashizan(self):
        """test method for tashizan
        """
        value1 = 2
        value2 = 6
        expected = 8
        actual = keisan.tashizan(value1, value2)
        self.assertEqual(expected, actual)



if __name__ == "__main__":
    unittest.main()