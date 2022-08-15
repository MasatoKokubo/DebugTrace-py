# simple_print_test.py
# (C) 2020 Masato Kokubo
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import unittest
from parameterized import parameterized
import debugtrace

class SimplePrintTest(unittest.TestCase):
    @parameterized.expand([
        (None , 'None'),
        (False, 'False'),
        (True , 'True'),
        ( 1   ,  '1'),
        (-1   , '-1'),
        ( 1.1 ,  '1.1'),
        (-1.1 , '-1.1'),
        ('A'    , "'A'"),
        ("'A'"  , "\"'A'\""),
        ('"A"'  , '\'"A"\''),
        ('"A\'' , "'\"A\\''"),
        ('ABCDE', "'ABCDE'"),
        ('\\'    , "'\\\\'"),
        ('\n'    , "'\\n'"),
        ('\r'    , "'\\r'"),
        ('\t'    , "'\\t'"),
        ('\x00\x01\x02\x03' , "'\\x00\\x01\\x02\\x03'"),
        ('\x04\x05\x06\x07' , "'\\x04\\x05\\x06\\x07'"),
        ('\x08\x09\x0A\x0B' , "'\\x08\\t\\n\\x0B'"),
        ('\x0C\x0D\x0E\x0F' , "'\\x0C\\r\\x0E\\x0F'"),
        ('\x10\x11\x12\x13' , "'\\x10\\x11\\x12\\x13'"),
        ('\x14\x15\x16\x17' , "'\\x14\\x15\\x16\\x17'"),
        ('\x18\x19\x1A\x1B' , "'\\x18\\x19\\x1A\\x1B'"),
        ('\x1C\x1D\x1E\x1F' , "'\\x1C\\x1D\\x1E\\x1F'"),
        (          b'\x00\x01\x02\x03'     , '(bytes)[00 01 02 03 | ....]'),
        (          b'\x30\x31\x32\x33\x34' , '(bytes)[30 31 32 33 34 | 01234]'),
        (bytearray(b'\x00\x01\x02\x03'    ), '(bytearray)[00 01 02 03 | ....]'),
        (bytearray(b'\x30\x31\x32\x33\x34'), '(bytearray)[30 31 32 33 34 | 01234]'),
        (date(2020, 3, 1), '2020-03-01'),
        (time( 1,  2,  3), '01:02:03'),
        (time(23, 48, 59), '23:48:59'),
        (datetime(2020, 3, 1, 1, 2, 3), '2020-03-01 01:02:03'),
        (datetime(2020, 3, 1, 1, 2, 3, 456789), '2020-03-01 01:02:03.456789'),
        (datetime(2020, 3, 1, 1, 2, 3, 456789, tzinfo=timezone(timedelta(hours=-9.25))), '2020-03-01 01:02:03.456789-09:15'),
        (datetime(2020, 3, 1, 1, 2, 3, 456789, tzinfo=timezone(timedelta(hours=-9   ))), '2020-03-01 01:02:03.456789-09:00'),
        (datetime(2020, 3, 1, 1, 2, 3, 456789, tzinfo=timezone(timedelta(hours= 0   ))), '2020-03-01 01:02:03.456789+00:00'),
        (datetime(2020, 3, 1, 1, 2, 3, 456789, tzinfo=timezone.utc                    ), '2020-03-01 01:02:03.456789+00:00'),
        (datetime(2020, 3, 1, 1, 2, 3, 456789, tzinfo=timezone(timedelta(hours=+9   ))), '2020-03-01 01:02:03.456789+09:00'),
        (datetime(2020, 3, 1, 1, 2, 3, 456789, tzinfo=timezone(timedelta(hours=+9.5 ))), '2020-03-01 01:02:03.456789+09:30'),
        ('end', "'end'")
    ])
    def test_print(self, value: object, expected: str) -> None:
        debugtrace.print('value', value)
        self.assertTrue(debugtrace.last_print_string().startswith(
            'value = ' + expected + ' (simple_print_test.py:'),
            msg=debugtrace.last_print_string())

if __name__ == '__main__':
    unittest.main()
