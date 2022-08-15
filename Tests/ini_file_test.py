# ini_file_test.py
# (C) 2020 Masato Kokubo
from __future__ import annotations
import unittest
from parameterized import parameterized
import debugtrace

class Node(object):
    def __init__(self, next: Node = None):
        self.next = next

class IniFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        debugtrace.init('./Tests/debugtrace_test.ini')

    maximum_data_output_width: int

    def setUp(self):
        global maximum_data_output_width
        maximum_data_output_width = debugtrace.main._config.maximum_data_output_width
        debugtrace.main._config.maximum_data_output_width = 140

    def cleanUp(self):
        debugtrace.main._config.maximum_data_output_width = maximum_data_output_width

    def func(self) -> None:
        _ = debugtrace.enter()
        self.assertRegex(debugtrace.last_print_string(),
            '_Enter_ func \\(ini_file_test.py:[0-9]+\\)')

    def func5(self) -> None:
        _ = debugtrace.enter()
        debugtrace.print('value', 5)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "||||||||value <= 5 "),
            msg=debugtrace.last_print_string())

    def func4(self) -> None:
        _ = debugtrace.enter()
        debugtrace.print('value', 4)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "||||||||value <= 4 "),
            msg=debugtrace.last_print_string())
        self.func5()

    def func3(self) -> None:
        _ = debugtrace.enter()
        debugtrace.print('value', 3)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "||||||value <= 3 "),
            msg=debugtrace.last_print_string())
        self.func4()

    def func2(self) -> None:
        _ = debugtrace.enter()
        debugtrace.print('value', 2)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "||||value <= 2 "),
            msg=debugtrace.last_print_string())
        self.func3()

    def func1(self) -> None:
        _ = debugtrace.enter()
        debugtrace.print('value', 1)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "||value <= 1 "),
            msg=debugtrace.last_print_string())
        self.func2()

    # enter_format
    # leave_format
    # maximum_indents
    def test_enter_leave(self) -> None:
        self.func()
        self.assertRegex(debugtrace.last_print_string(),
            '_Leave_ func \\(ini_file_test.py:[0-9]+\\) duration: 0:00:00\\.[0-9]+')

        self.func1()

    # indent_string
    # print_suffix_format
    def test_indent_string(self) -> None:
        _ = debugtrace.enter()
        debugtrace.print('foo')
        self.assertRegex(debugtrace.last_print_string(), '||foo \\(ini_file_test.py::[0-9]+\\)')

    # data_indent_string
    # maximum_data_output_width
    def test_data_indent_string(self) -> None:
        debugtrace.main._config.maximum_data_output_width = 30
        debugtrace.LogBuffer.maximum_data_output_width = 30

        debugtrace.print('value', [1111, 2222, 3333, 4444, 5555])
        self.assertTrue(debugtrace.last_print_string().startswith(
            "value <= (_count_:5)[\n``1111, 2222, 3333, 4444, 5555\n] "),
            msg=debugtrace.last_print_string())

    # cyclic_reference_string
    # key_value_separator
    # reflection_nest_limit
    def test_cyclic_reference_string(self) -> None:
        # cyclic_reference_string
        node = Node()
        node.next = node
        debugtrace.print('node1', node)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "node1 <= (__main__.Node){next:: <CyclicReference>} "),
            msg=debugtrace.last_print_string())

        node = Node(Node())
        debugtrace.print('node2', node)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "node2 <= (__main__.Node){next:: (__main__.Node){next:: None}} "),
            msg=debugtrace.last_print_string())

        # reflection_nest_limit
        node = Node(Node(Node()))
        debugtrace.print('node3', node)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "node3 <= (__main__.Node){next:: (__main__.Node){next:: (__main__.Node){next:: None}}} "),
            msg=debugtrace.last_print_string())

        node = Node(Node(Node(Node())))
        debugtrace.print('node4', node)
        self.assertTrue(debugtrace.last_print_string().startswith(
            "node4 <= (__main__.Node){next:: (__main__.Node){next:: (__main__.Node){next:: <Limit>}}} "),
            msg=debugtrace.last_print_string())

    # data_indent_string
    # limit_string
    # varname_value_separator
    # key_value_separator
    # count_format
    # minimum_output_count
    # bytes_count_in_line
    # collection_limit
    # bytes_limit
    # string_limit
    @parameterized.expand([
        # tuple
        ((1, 2, 3, 4)         , "(1, 2, 3, 4) "),
        ((1, 2, 3, 4, 5)      , "(_count_:5)(1, 2, 3, 4, 5) "),
        ((1, 2, 3, 4, 5, 6)   , "(_count_:6)(1, 2, 3, 4, 5, 6) "),
        ((1, 2, 3, 4, 5, 6, 7), "(_count_:7)(1, 2, 3, 4, 5, 6, <Limit>) "),

        # list
        ([1, 2, 3, 4]         , "[1, 2, 3, 4] "),
        ([1, 2, 3, 4, 5]      , "(_count_:5)[1, 2, 3, 4, 5] "),
        ([1, 2, 3, 4, 5, 6]   , "(_count_:6)[1, 2, 3, 4, 5, 6] "),
        ([1, 2, 3, 4, 5, 6, 7], "(_count_:7)[1, 2, 3, 4, 5, 6, <Limit>] "),

        # dict
        ({1:'A',2:'B',3:'C',4:'D'}                  , "{1:: 'A', 2:: 'B', 3:: 'C', 4:: 'D'} "),
        ({1:'A',2:'B',3:'C',4:'D',5:'E'}            , "(_count_:5){1:: 'A', 2:: 'B', 3:: 'C', 4:: 'D', 5:: 'E'} "),
        ({1:'A',2:'B',3:'C',4:'D',5:'E',6:'F'}      , "(_count_:6){1:: 'A', 2:: 'B', 3:: 'C', 4:: 'D', 5:: 'E', 6:: 'F'} "),
        ({1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G'}, "(_count_:7){1:: 'A', 2:: 'B', 3:: 'C', 4:: 'D', 5:: 'E', 6:: 'F', <Limit>} "),

        # bytes
        (b'\x40'                            , "(bytes)[40 | @] "),
        (b'\x40\x41'                        , "(bytes)[40 41 | @A] "),
        (b'\x40\x41\x42'                    , "(bytes)[40 41 42 | @AB] "),
        (b'\x40\x41\x42\x43'                , "(bytes)[\n``40 41 42 43 | @ABC\n] "),
        (b'\x40\x41\x42\x43\x44'            , "(bytes)[\n``40 41 42 43 | @ABC\n``44          | D\n] "),
        (b'\x40\x41\x42\x43\x44\x45'        , "(bytes _length_:6)[\n``40 41 42 43 | @ABC\n``44 45       | DE\n] "),
        (b'\x40\x41\x42\x43\x44\x45\x46'    , "(bytes _length_:7)[\n``40 41 42 43 | @ABC\n``44 45 46    | DEF\n] "),
        (b'\x40\x41\x42\x43\x44\x45\x46\x47', "(bytes _length_:8)[\n``40 41 42 43 | @ABC\n``44 45 46 <Limit>| DEF\n] "),

        # bytearray
        (bytearray(b'\x40'                            ), "(bytearray)[40 | @] "),
        (bytearray(b'\x40\x41'                        ), "(bytearray)[40 41 | @A] "),
        (bytearray(b'\x40\x41\x42'                    ), "(bytearray)[40 41 42 | @AB] "),
        (bytearray(b'\x40\x41\x42\x43'                ), "(bytearray)[\n``40 41 42 43 | @ABC\n] "),
        (bytearray(b'\x40\x41\x42\x43\x44'            ), "(bytearray)[\n``40 41 42 43 | @ABC\n``44          | D\n] "),
        (bytearray(b'\x40\x41\x42\x43\x44\x45'        ), "(bytearray _length_:6)[\n``40 41 42 43 | @ABC\n``44 45       | DE\n] "),
        (bytearray(b'\x40\x41\x42\x43\x44\x45\x46'    ), "(bytearray _length_:7)[\n``40 41 42 43 | @ABC\n``44 45 46    | DEF\n] "),
        (bytearray(b'\x40\x41\x42\x43\x44\x45\x46\x47'), "(bytearray _length_:8)[\n``40 41 42 43 | @ABC\n``44 45 46 <Limit>| DEF\n] "),

        # string
        ('ABCDE'      , "'ABCDE'"),
        ('ABCDEF'     , "(_length_:6)'ABCDEF'"),
        ('ABCDEFGHIJ' , "(_length_:10)'ABCDEFGHIJ'"),
        ('ABCDEFGHIJK', "(_length_:11)'ABCDEFGHIJ<Limit>'"),

        ('end', "'end'")
    ])
    def test_print(self, value: object, expected: str) -> None:
        debugtrace.print('value', value)
        self.assertTrue(debugtrace.last_print_string().startswith('value <= ' + expected),
            msg=debugtrace.last_print_string())

if __name__ == '__main__':
    unittest.main()
