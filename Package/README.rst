#################
DebugTrace-python
#################

**DebugTrace-python** is a library that outputs trace logs
when debugging your Python programs.
It supports Python 3.7 or later.
By embedding "``_ = debugtrace.enter()``" at the start of the method,
you can output the execution status of the program under development.

1. Features
===========

* Automatically outputs the method name, source file name and line number
  of invokers of ``debugtrace.enter`` function.
* Also outputs end logs when the scope ends.
* Indents logs automatically with nested methods and objects.
* Automatically line breaks in value output.
* Uses reflection to output content even for objects of classes
  that do not implement the ``__str__`` method.
* You can customize output contents by setting ``debugtrace.ini`` file.
* You can select sys.stdout, sys.stderr or logging.Logger to output.

2. Install
==========

``pip install debugtrace``

3. How to use
=============

Do the following for the debug target and related functions and methods:

* Insert "``_ = debugtrace.enter()``" at the beginning of functions and methods.
* Insert "``debugtrace.print('foo', foo)``" to output variables to the log if necessary.

The following is an example of a Python program using DebugTrace-py and a log when it is executed.

::

    # ReadmeExample.py
    import datetime
    import debugtrace # for Debugging

    # Contact class
    class Contact(object):
        def __init__(self, id: int, firstName: str, lastName: str, birthday: datetime.date) -> None:
            _ = debugtrace.enter(self) # for Debugging
            self.id = id
            self.firstName = firstName
            self.lastName  = lastName
            self.birthday  = birthday

    def func2():
        _ = debugtrace.enter() # for Debugging
        contact = [
            Contact(1, 'Akane' , 'Apple', datetime.date(1991, 2, 3)),
            Contact(2, 'Yukari', 'Apple', datetime.date(1992, 3, 4))
        ]
        debugtrace.print('contact', contact) # for Debugging

    def func1():
        _ = debugtrace.enter() # for Debugging
        func2()

    func1()

Log output contents:
::

    2020-07-19 11:39:53.708348 DebugTrace-python 1.0.1
    2020-07-19 11:39:53.708415   config file path: <No config file>
    2020-07-19 11:39:53.708427 　logger: sys.stderr
    2020-07-19 11:39:53.708435 
    2020-07-19 11:39:53.712857 Enter func1 (ReadmeExample.py:23)
    2020-07-19 11:39:53.713020 | Enter func2 (ReadmeExample.py:15)
    2020-07-19 11:39:53.713114 | | Enter Contact.__init__ (ReadmeExample.py:8)
    2020-07-19 11:39:53.713171 | | Leave Contact.__init__ (ReadmeExample.py:8) duration: 0:00:00.000009
    2020-07-19 11:39:53.713242 | | 
    2020-07-19 11:39:53.713279 | | Enter Contact.__init__ (ReadmeExample.py:8)
    2020-07-19 11:39:53.713322 | | Leave Contact.__init__ (ReadmeExample.py:8) duration: 0:00:00.000004
    2020-07-19 11:39:53.713889 | | 
    2020-07-19 11:39:53.713937 | | contact = (list)[
    2020-07-19 11:39:53.713956 | |   (__main__.Contact){
    2020-07-19 11:39:53.713981 | |     birthday: 1991-02-03, firstName: (length:5)'Akane', id: 1,
    2020-07-19 11:39:53.714007 | |     lastName: (length:5)'Apple'
    2020-07-19 11:39:53.714032 | |   },
    2020-07-19 11:39:53.714057 | |   (__main__.Contact){
    2020-07-19 11:39:53.714081 | |     birthday: 1992-03-04, firstName: (length:6)'Yukari', id: 2,
    2020-07-19 11:39:53.714107 | |     lastName: (length:5)'Apple'
    2020-07-19 11:39:53.714120 | |   }
    2020-07-19 11:39:53.714128 | | ] (ReadmeExample.py:20)
    2020-07-19 11:39:53.714144 | | 
    2020-07-19 11:39:53.714180 | Leave func2 (ReadmeExample.py:15) duration: 0:00:00.001086
    2020-07-19 11:39:53.714223 Leave func1 (ReadmeExample.py:23) duration: 0:00:00.001289

4. Functions
============

There are mainly the following functions.

.. list-table:: Function list
    :widths: 10, 90
    :header-rows: 1

    * - Name
      - Discription
    * - ``enter``
      - | Outputs an entering log.
        | Also outputs a leaving log at the end of the code block.
        |
        | *Arguments*:
        | **invoker** (``object optional``): Pass the self or cls of the invoker. (Optional)
        |
        | *Examples*:
        | ``_ = debugtrace.enter(self)``
        | ``_ = debugtrace.enter(cls)``
        | ``_ = debugtrace.enter()``
    * - ``print``
      - | Outputs the variable name and value.
        |
        | *Arguments*:
        | **name** (str): Variable name, etc.
        | **value** (object): Output value
        | **output_private** (bool): Output private member if True (default: False)
        | **output_method** (bool): Output method if True (default: False)
        |
        | The following are keyword arguments and can be omitted.
        |
        | **force_reflection** (``bool``): If true, outputs using reflection even if it has a ``__str__`` or ``__repr__`` method (default: ``False``)
        | **output_private** (``bool``): If true, also outputs private members when using reflection (default: ``False``)
        | **output_method** (``bool``): If true, also outputs method members when using reflection (default: ``False``)
        | **collection_limit** (``int``): The limit value of elements such as ``list``, ``tuple`` and ``dict`` to output (default: ``None``)
        | **bytes_limit** (``int``):  The limit value of elements for ``bytes`` and ``bytearray`` to output (default: ``None``)
        | **string_limit** (``int``): The limit value of characters for string to output (default: ``None``)
        | **reflection_nest_limit** (int): The The limit value for reflection nesting (default: ``None``)
        |
        | *Examples*:
        | ``debugtrace.print('Hellow')``
        | ``debugtrace.print('foo', foo)``
        | ``debugtrace.print('foo', foo, force_reflection=True)``
        | ``debugtrace.print('foos', foos, collection_limit=1024)``

5. Options that can be specified in the **debugtrace.ini** file
===============================================================

DebugTrace-python reads the ``debugtrace.ini`` file
in the current directory for initialization.
The section is ``[debugtrace]``.

You can specify the following options in the ``debugtrace.ini`` file.

.. list-table:: ``debugtrace.ini``
    :widths: 30, 50, 20
    :header-rows: 1

    * - Option Name
      - Description
      - Default Value
    * - ``logger``
      - | The logger used by debugtrace
        | ``StdOut: Output to sys.stdout``
        | ``StdErr: Output to sys.stderr``
        | ``Logger: Output using logging package``
      - ``StdErr``
    * - ``logging_config_file``
      - The configuration file name specified in logging package
      - ``logging.conf``
    * - ``logging_logger_name``
      - The logger name when using the logging package
      - ``debugtrace``
    * - ``logging_level``
      - The log level when using the logging package
      - ``DEBUG``
    * - ``is_enabled``
      - | ``False: Log output is disabled``
        | ``True: Log output is enabled``
      - ``True``
    * - ``enter_format``
      - | The format string of log output when entering functions or methods
        | ``{0}: The function or method name``
        | ``{1}: The file name``
        | ``{2}: The line number``
      - ``Enter {0} ({1}:{2})``
    * - ``leave_format``
      - | The format string of log output when leaving functions or methods
        | ``{0}: The function or method name``
        | ``{1}: The file name``
        | ``{2}: The line number``
        | ``{3}: The time from entering``
      - ``Leave {0} ({1}:{2}) duration: {3}``
    * - ``maximum_indents``
      - The maximum number of indents
      - ``20``
    * - ``indent_string``
      - The indentation string for code
      - ``|\s``
    * - ``data_indent_string``
      - The indentation string for data
      - ``\s\s``
    * - ``limit_string``
      - The string to represent that it has exceeded the limit
      - ``...``
    * - ``non_output_string``
      - | The string to be output instead of not outputting value
        | (Currently unused)
      - ``...``
    * - ``cyclic_reference_string``
      - The string to represent that the cyclic reference occurs
      - ``*** Cyclic Reference ***``
    * - ``varname_value_separator``
      - The separator string between the variable name and value
      - ``\s=\s``
    * - ``key_value_separator``
      - The separator string between the key and value of dictionary and between the attribute name and value
      - ``:\s``
    * - ``print_suffix_format``
      - The format string of ``print`` method suffix
      - ``\s({1}:{2})``
    * - ``count_format``
      - The format string of the number of elements such as ``list``, ``tuple`` and ``dict``
      - ``count:{}``
    * - ``minimum_output_count``
      - The minimum value to output the number of elements such as ``list``, ``tuple`` and ``dict``
      - ``5``
    * - ``length_format``
      - The format string of the length of string and ``bytes``
      - ``length:{}``
    * - ``minimum_output_length``
      - The minimum value to output the length of string and ``bytes``
      - ``5``
    * - ``log_datetime_format``
      - | Log date and time format when ``logger`` is ``StdOut`` or ``StdErr``
        | (Currently not configurable)
      - ``%Y-%m-%d %H:%M:%S.%f``
    * - ``maximum_data_output_width``
      - The maximum output width of data
      - ``70``
    * - ``bytes_count_in_line``
      - The count in line of ``bytes``
      - ``16``
    * - ``collection_limit``
      - The limit value of elements such as ``list``, ``tuple`` and ``dict`` to output
      - ``512``
    * - ``bytes_limit``
      - The limit value of elements for ``bytes`` and ``bytearray``  to output
      - ``8192``
    * - ``string_limit``
      - The limit value of characters for string to output
      - ``8192``
    * - ``reflection_nest_limit``
      - The The limit value for reflection nesting
      - ``4``

*Converts* ``\s`` *to space.*

6. License
==========

MIT License (MIT)

7. Release notes
================

``DebugTrace-python 1.0.1 - July 19, 2020``
------------------------------------------------

* Improved the line break handling of data output.

``DebugTrace-python 1.0.0 - May 26, 2020``
------------------------------------------------

* First release

*(C) 2020 Masato Kokubo*
