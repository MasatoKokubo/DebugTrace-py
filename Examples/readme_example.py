# readme_example.py
import datetime
import debugtrace

class Contact(object):
    def __init__(self, id: int, firstName: str, lastName: str, birthday: datetime.date) -> None:
        _ = debugtrace.enter(self)
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.birthday = birthday

def func2():
    _ = debugtrace.enter()
    contacts = [
        Contact(1, 'Akane' , 'Apple', datetime.date(1991, 2, 3)),
        Contact(2, 'Yukari', 'Apple', datetime.date(1992, 3, 4))
    ]
    debugtrace.print('contacts', contacts)

def func1():
    _ = debugtrace.enter()
    debugtrace.print('Hello, World!')
    func2()

func1()
