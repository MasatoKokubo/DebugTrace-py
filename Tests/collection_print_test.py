from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import unittest
from parameterized import parameterized
import debugtrace

class CollectionPrintTest(unittest.TestCase):
    @parameterized.expand([
        ((), '(tuple)()'),
        ((1,), '(tuple)(1)'),
        ((1, 2, 3), '(tuple)(1, 2, 3)'),
        ((1, 2, (3, 4, 5)), '(tuple)(1, 2, (tuple)(3, 4, 5))'),
        ([], '(list)[]'),
        ([1], '(list)[1]'),
        ([1, 2, 3], '(list)[1, 2, 3]'),
        ([1, 2, [3, 4, 5]], '(list)[1, 2, (list)[3, 4, 5]]'),
        (set(), '(set){}'),
        ({1}, '(set){1}'),
        ({1, 2, 3}, '(set){1, 2, 3}'),
        ({}, '(dict){}'),
        ({1: 'A'}, "(dict){1: 'A'}"),
        ({1: 'A', 2: 'B', 3: 'C'}, "(dict){1: 'A', 2: 'B', 3: 'C'}"),
        ({1: 'A', 2: 'B', 3: {4: 'D', 5: 'E', 6: 'F'}}, "(dict){1: 'A', 2: 'B', 3: (dict){4: 'D', 5: 'E', 6: 'F'}}"),
        ('end', "'end'")
    ])
    def test_print(self, value: object, result: str) -> None:
        debugtrace.print('value', value)
        self.assertEqual(len(debugtrace.main._last_print_strings), 1)
        self.assertEqual(debugtrace.main._last_print_strings[0], 'value = ' + result)

if __name__ == '__main__':
    unittest.main()
