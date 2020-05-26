from __future__ import annotations
import unittest
from parameterized import parameterized
import debugtrace

class Point(object):
    __slots__ = ['_x', '_y']

    def __init__(self, x:int, y:int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def transpose(self) -> __class__:
        return Point(self._y, self._x)

    def __str__(self) -> str:
        return '(' + str(self._x) + ', ' + str(self._y) + ')'

class Point3(object):
    __slots__ = ['_x', '_y', '_z']

    def __init__(self, x:int, y:int, z:int) -> None:
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def z(self) -> int:
        return self._z

    def __repr__(self) -> str:
        return '(' + str(self._x) + ', ' + str(self._y) + ', ' + str(self._z) + ')'

class N(object):
    def __init__(self, n: __class__ = None):
        self.n = n

class PrintOptionTest(unittest.TestCase):
    maximum_data_output_width: int

    def setUp(self):
        global maximum_data_output_width
        maximum_data_output_width = debugtrace.main._maximum_data_output_width
        debugtrace.main._maximum_data_output_width = 140

    def cleanUp(self):
        debugtrace.main._maximum_data_output_width = maximum_data_output_width

    # force_reflection
    def test_force_reflection(self) -> None:
        point = Point(1, 2)
        debugtrace.print('point', point)
        self.assertTrue(debugtrace.last_print_string().find('point = str(): (1, 2)') >= 0,
            msg=debugtrace.last_print_string())

        debugtrace.print('point', point, force_reflection=True)
        self.assertTrue(debugtrace.last_print_string().find('point = (__main__.Point){x: 1, y: 2}') >= 0,
            msg=debugtrace.last_print_string())

        point3 = Point3(1, 2, 3)
        debugtrace.print('point3', point3)
        self.assertTrue(debugtrace.last_print_string().find('point3 = repr(): (1, 2, 3)') >= 0,
            msg=debugtrace.last_print_string())

        debugtrace.print('point3', point3, force_reflection=True)
        self.assertTrue(debugtrace.last_print_string().find('point3 = (__main__.Point3){x: 1, y: 2, z: 3}') >= 0,
            msg=debugtrace.last_print_string())

    # output_private
    def test_output_private(self) -> None:
        point = Point(1, 2)
        debugtrace.print('point', point, force_reflection=True, output_private=True)
        self.assertTrue(debugtrace.last_print_string().find('point = (__main__.Point){_x: 1, _y: 2, x: 1, y: 2}') >= 0,
            msg=debugtrace.last_print_string())

    # output_method
    def test_output_method(self) -> None:
        point = Point(1, 2)
        debugtrace.print('point', point, force_reflection=True, output_method=True)
        self.assertTrue(debugtrace.last_print_string().find('point = (__main__.Point){transpose: (method){}, x: 1, y: 2}') >= 0,
            msg=debugtrace.last_print_string())

    # collection_limit
    @parameterized.expand([
        (None, 'values = (list count:5)[1, 2, 3, 4, 5]'),
        (   4, 'values = (list count:5)[1, 2, 3, 4, ...]'),
        (   1, 'values = (list count:5)[1, ...]'),
        (   0, 'values = (list count:5)[...]'),
        (  -1, 'values = (list count:5)[...]')
    ])
    def test_collection_limit(self, limit: int, expected: str) -> None:
        values = [1, 2, 3, 4, 5]
        debugtrace.print('values', values, collection_limit=limit)
        self.assertTrue(debugtrace.last_print_string().find(expected) >= 0,
            msg=debugtrace.last_print_string())

    # string_limit
    @parameterized.expand([
        (None, "string = (length:5)'ABCDE'"),
        (   4, "string = (length:5)'ABCD...'"),
        (   1, "string = (length:5)'A...'"),
        (   0, "string = (length:5)'...'"),
        (  -1, "string = (length:5)'...'")
    ])
    def test_string_limit(self, limit: int, expected: str) -> None:
        string = "ABCDE"
        debugtrace.print('string', string, string_limit=limit)
        self.assertTrue(debugtrace.last_print_string().find(expected) >= 0,
            msg=debugtrace.last_print_string())

    # bytes_limit
    @parameterized.expand([
        (None, 'bytes_ = (bytes length:5)[41 42 43 44 45 | ABCDE]'),
        (   4, 'bytes_ = (bytes length:5)[41 42 43 44 ...| ABCD]'),
        (   1, 'bytes_ = (bytes length:5)[41 ...| A]'),
        (   0, 'bytes_ = (bytes length:5)[...| ]'),
        (  -1, 'bytes_ = (bytes length:5)[...| ]')
    ])
    def test_bytes_limit(self, limit: int, expected: str) -> None:
        bytes_ = b'\x41\x42\x43\x44\x45'
        debugtrace.print('bytes_', bytes_, bytes_limit=limit)
        self.assertTrue(debugtrace.last_print_string().find(expected) >= 0,
            msg=debugtrace.last_print_string())

    # reflection_nest_limit
    @parameterized.expand([
        (None, 'n = (__main__.N){n: (__main__.N){n: (__main__.N){n: (__main__.N){n: (__main__.N){n: ...}}}}}'),
        (   3, 'n = (__main__.N){n: (__main__.N){n: (__main__.N){n: (__main__.N){n: ...}}}}'),
        (   2, 'n = (__main__.N){n: (__main__.N){n: (__main__.N){n: ...}}}'),
        (   1, 'n = (__main__.N){n: (__main__.N){n: ...}}'),
        (   0, 'n = (__main__.N){n: ...}'),
        (  -1, 'n = ...')
    ])
    def test_reflection_nest_limit(self, limit: int, expected: str) -> None:
        n = N(N(N(N(N(N())))))
        debugtrace.print('n', n, reflection_nest_limit=limit)
        self.assertTrue(debugtrace.last_print_string().find(expected) >= 0,
            msg=debugtrace.last_print_string())

if __name__ == '__main__':
    unittest.main()
