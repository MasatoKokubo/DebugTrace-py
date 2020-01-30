# ReadmeExample.py
import datetime
import debugtrace # for Debugging

# Contact class
class Contact(object):
    def __init__(self, id: int, firstName: str, lastName: str, birthday: datetime.date) -> None:
        self.id = id
        self.firstName = firstName
        self.lastName  = lastName
        self.birthday  = birthday

def func2():
    _ = debugtrace.enter() # for Debugging
    contact = [
        Contact(1, "Akane" , "Apple", datetime.date(1991, 2, 3)),
        Contact(2, "Yukari", "Apple", datetime.date(1992, 3, 4))
    ]
    debugtrace.print("contact", contact) # for Debugging

def func1():
    _ = debugtrace.enter() # for Debugging
    func2()

func1()
