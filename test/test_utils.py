import unittest

from date_utils import get_beginning_of_current_week, get_end_of_current_week


class TestDateUtils(unittest.TestCase):
    def test_01_week_start_and_end(self):
        get_beginning_of_current_week()
        get_end_of_current_week()


if __name__ == "__main__":
    unittest.main(verbosity=2)