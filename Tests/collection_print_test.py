# collection_print_test.py
import unittest
from parameterized import parameterized
import debugtrace

class CollectionPrintTest(unittest.TestCase):
    @parameterized.expand([
        ((), '()'),
        ((1,), '(1,)'),
        ((1, 2, 3), '(1, 2, 3)'),
        ((1, 2, (3, 4, 5)), '(1, 2, (3, 4, 5))'),
        ([], '[]'),
        ([1], '[1]'),
        ([1, 2, 3], '[1, 2, 3]'),
        ([1, 2, [3, 4, 5]], '[1, 2, [3, 4, 5]]'),
        (set(), '{}'),
        ({1}, '{1}'),
        ({1, 2, 3}, '{1, 2, 3}'),
        (frozenset([]), '(frozenset){}'), # since 1.1.0
        (frozenset([1]), '(frozenset){1}'), # since 1.1.0
        (frozenset([1, 2, 3]), '(frozenset){1, 2, 3}'), # since 1.1.0
        ({}, '{:}'),
        ({1: 'A'}, "{1: 'A'}"),
        ({1: 'A', 2: 'B', 3: 'C'}, "{1: 'A', 2: 'B', 3: 'C'}"),
        ({1: 'A', 2: 'B', 3: {4: 'D', 5: 'E', 6: 'F'}}, "{1: 'A', 2: 'B', 3: {4: 'D', 5: 'E', 6: 'F'}}"),
        ('end', "'end'")
    ])
    def test_print(self, value: object, expected: str) -> None:
        debugtrace.print('value', value)
        self.assertTrue(debugtrace.last_print_string().startswith(
            'value = ' + expected + ' (collection_print_test.py:'),
            msg=debugtrace.last_print_string())

if __name__ == '__main__':
    unittest.main()
