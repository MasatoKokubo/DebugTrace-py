from datetime import date
import unittest
import debugtrace

class Contact(object):
    __slots__ = ['first_name', 'last_name', 'birthday', 'phone_number']

    def __init__(self, first_name: str, last_name: str, birthday: date, phone_number: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.phone_number = phone_number

class Contacts(object):
    __slots__ = ['contact1', 'contact2', 'contact3', 'contact4']

    def __init__(self, contact1: Contact, contact2: Contact, contact3: Contact, contact4: Contact) -> None:
        self.contact1 = contact1
        self.contact2 = contact2
        self.contact3 = contact3
        self.contact4 = contact4

class LineBreakTest(unittest.TestCase):
#   @classmethod
#   def setUpClass(cls):
#       debugtrace.init('./Tests/debugtrace_test.ini')

    maximum_data_output_width: int

    def setUp(self):
        global maximum_data_output_width
        maximum_data_output_width = debugtrace.main._maximum_data_output_width
        debugtrace.main._maximum_data_output_width = 60

    def cleanUp(self):
        debugtrace.main._maximum_data_output_width = maximum_data_output_width


    def test_line_break_of_iterable(self) -> None:
        contacts = [
            Contact('Akane' , 'Apple' , (2020, 1, 1), '080-1111-1111'),
            Contact('Yukari', 'Apple' , (2020, 2, 2), '080-2222-2222'),
            None,
            None
        ]

        _ = debugtrace.enter()
        debugtrace.print('contacts', contacts)
        self.assertTrue('[\n  (__main__.Contact){' in debugtrace.last_print_string())
        self.assertTrue('  birthday:'     in debugtrace.last_print_string())
        self.assertTrue(', first_name: '  in debugtrace.last_print_string())
        self.assertTrue('  last_name:'    in debugtrace.last_print_string())
        self.assertTrue('  phone_number:' in debugtrace.last_print_string())
        self.assertTrue('},\n  (__main__.Contact){' in debugtrace.last_print_string())
        self.assertTrue('},\n  None, None' in debugtrace.last_print_string())

    def test_line_break_of_refrection(self) -> None:
        contacts = Contacts(
            Contact('Akane' , 'Apple' , (2020, 1, 1), '080-1111-1111'),
            Contact('Yukari', 'Apple' , (2020, 2, 2), '080-2222-2222'),
            None,
            None
        )

        _ = debugtrace.enter()
        debugtrace.print('contacts', contacts)
        self.assertTrue('{\n  contact1: (__main__.Contact){' in debugtrace.last_print_string())
        self.assertTrue('  birthday:'     in debugtrace.last_print_string())
        self.assertTrue(', first_name: '  in debugtrace.last_print_string())
        self.assertTrue('  last_name:'    in debugtrace.last_print_string())
        self.assertTrue('  phone_number:' in debugtrace.last_print_string())
        self.assertTrue('},\n  contact2: (__main__.Contact){' in debugtrace.last_print_string())
        self.assertTrue('},\n  contact3: None, contact4: None' in debugtrace.last_print_string())

if __name__ == '__main__':
    unittest.main()
