# ReadmeExample.py
import datetime
import debugtrace # ToDo: Remove after debugging

class Contact(object):
    def __init__(self, id: int, firstName: str, lastName: str, birthday: datetime.date) -> None:
        _ = debugtrace.enter(self) # ToDo: Remove after debugging
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.birthday = birthday

def func2():
    _ = debugtrace.enter() # ToDo: Remove after debugging
    contacts = [
        Contact(1, 'Akane' , 'Apple', datetime.date(1991, 2, 3)),
        Contact(2, 'Yukari', 'Apple', datetime.date(1992, 3, 4))
    ]
    debugtrace.print('contacts', contacts) # ToDo: Remove after debugging

def func1():
    _ = debugtrace.enter() # ToDo: Remove after debugging
    debugtrace.print('Hello, World!') # ToDo: Remove after debugging
    func2()

func1()
