import unittest
import datetime
from dateutil import tz

from date_utils import get_beginning_of_current_week, get_end_of_current_week, get_date_from_string


class TestDateUtils(unittest.TestCase):
    def test_01_week_start_and_end(self):
        get_beginning_of_current_week()
        get_end_of_current_week()

    def test_02_get_datetime_from_string(self):
        # 2022-11-23T16:00:00+02:00
        sast = tz.gettz("Africa/Johannesburg")
        peza_bd_date = datetime.datetime(1992, 3, 25, tzinfo=sast)
        bd_str = peza_bd_date.strftime("%Y-%m-%dT%H:%M:%S%z")
        bd_date = get_date_from_string(bd_str)
        self.assertEqual(
            peza_bd_date,
            bd_date
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)