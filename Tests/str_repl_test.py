# str_repl_test.py
# (C) 2020 Masato Kokubo
import unittest
import debugtrace

class Person1(object):
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

class Person2(object):
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __str__(self) -> str:
        return self.full_name

class Person3(object):
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __repr__(self) -> str:
        return self.full_name

class Person4(object):
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return self.full_name

class ClassTest(unittest.TestCase):
    minimum_output_length: int

    def setUp(self):
        global minimum_output_length
        minimum_output_length = debugtrace.main._config.minimum_output_length
        debugtrace.main._config.minimum_output_length = 64

    def cleanUp(self):
        debugtrace.main._config.minimum_output_length = minimum_output_length

    def test_no__str__repr__(self) -> None:
        _ = debugtrace.enter()
        person = Person1('First', 'Last')
        debugtrace.print('person', person)
        self.assertTrue("first_name: 'First'" in debugtrace.last_print_string())
        self.assertTrue("last_name: 'Last'" in debugtrace.last_print_string())
        self.assertTrue("full_name: 'First Last'" in debugtrace.last_print_string())

    def test__str__(self) -> None:
        _ = debugtrace.enter()
        person = Person2('First', 'Last')
        debugtrace.print('person', person)
        self.assertTrue("person = str(): First Last" in debugtrace.last_print_string())

    def test__repr__(self) -> None:
        _ = debugtrace.enter()
        person = Person3('First', 'Last')
        debugtrace.print('person', person)
        self.assertTrue("person = repr(): First Last" in debugtrace.last_print_string())

    def test__str__repr__(self) -> None:
        _ = debugtrace.enter()
        person = Person4('First', 'Last')
        debugtrace.print('person', person)
        self.assertTrue("person = repr(): First Last" in debugtrace.last_print_string())

if __name__ == '__main__':
    unittest.main()
