# ReadmeExample.py
import datetime
import debugtrace # for Debugging

class Contact(object):
    def __init__(self, id: int, firstName: str, lastName: str, birthday: datetime.date) -> None:
        _ = debugtrace.enter(self) # for Debugging
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.birthday = birthday

def func2():
    _ = debugtrace.enter() # for Debugging
    contacts = [
        Contact(1, "Akane" , "Apple", datetime.date(1991, 2, 3)),
        Contact(2, "Yukari", "Apple", datetime.date(1992, 3, 4))
    ]
    debugtrace.print("contacts", contacts) # for Debugging

def func1():
    _ = debugtrace.enter() # for Debugging
    func2()

func1()
