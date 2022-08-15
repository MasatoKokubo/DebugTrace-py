#############
DebugTrace-py
#############

**DebugTrace-py** is a library that outputs trace logs
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

    # readme_example.py
    import datetime
    import debugtrace # TODO: Remove after debugging

    # Contact class
    class Contact(object):
        def __init__(self, id: int, firstName: str, lastName: str, birthday: datetime.date) -> None:
            _ = debugtrace.enter(self) # TODO: Remove after debugging
            self.id = id
            self.firstName = firstName
            self.lastName  = lastName
            self.birthday  = birthday

    def func2():
        _ = debugtrace.enter() # TODO: Remove after debugging
        contact = [
            Contact(1, 'Akane' , 'Apple', datetime.date(1991, 2, 3)),
            Contact(2, 'Yukari', 'Apple', datetime.date(1992, 3, 4))
        ]
        debugtrace.print('contact', contact) # TODO: Remove after debugging

    def func1():
        _ = debugtrace.enter() # TODO: Remove after debugging
        debugtrace.print('Hello, World!') # TODO: Remove after debugging
        func2()

    func1()

Log output contents:

::

    2022-08-15 13:19:11.080752 DebugTrace-py 1.2.0 on Python 3.10.4
    2022-08-15 13:19:11.080803   config file path: <No config file>
    2022-08-15 13:19:11.080834   logger: sys.stderr
    2022-08-15 13:19:11.080901 
    2022-08-15 13:19:11.080926 ______________________________ MainThread #139879021757504 ______________________________
    2022-08-15 13:19:11.080953 
    2022-08-15 13:19:11.081716 Enter func1 (readme_example.py:22)
    2022-08-15 13:19:11.081791 | Hello, World! (readme_example.py:23)
    2022-08-15 13:19:11.081853 | Enter func2 (readme_example.py:14)
    2022-08-15 13:19:11.081919 | | Enter Contact.__init__ (readme_example.py:7)
    2022-08-15 13:19:11.081964 | | Leave Contact.__init__ (readme_example.py:7) duration: 0:00:00.000010
    2022-08-15 13:19:11.082032 | | 
    2022-08-15 13:19:11.082059 | | Enter Contact.__init__ (readme_example.py:7)
    2022-08-15 13:19:11.082105 | | Leave Contact.__init__ (readme_example.py:7) duration: 0:00:00.000009
    2022-08-15 13:19:11.082439 | | 
    2022-08-15 13:19:11.082467 | | contacts = [
    2022-08-15 13:19:11.082498 | |   (__main__.Contact){
    2022-08-15 13:19:11.082521 | |     birthday: 1991-02-03, firstName: 'Akane', id: 1, lastName: 'Apple'
    2022-08-15 13:19:11.082543 | |   },
    2022-08-15 13:19:11.082566 | |   (__main__.Contact){
    2022-08-15 13:19:11.082595 | |     birthday: 1992-03-04, firstName: 'Yukari', id: 2, lastName: 'Apple'
    2022-08-15 13:19:11.082618 | |   }
    2022-08-15 13:19:11.082638 | | ] (readme_example.py:19)
    2022-08-15 13:19:11.082651 | | 
    2022-08-15 13:19:11.082678 | Leave func2 (readme_example.py:14) duration: 0:00:00.000792
    2022-08-15 13:19:11.082709 Leave func1 (readme_example.py:22) duration: 0:00:00.000957

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

DebugTrace-py reads the ``debugtrace.ini`` file
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
        |
        | Specifiable Values:
        | ``stdout -`` Output to ``sys.stdout``
        | ``stderr -`` Output to ``sys.stderr``
        | ``logger -`` Output using ``logging`` package
        | ``file:`` <log file path> ``-`` Output directly to the file
      - ``stderr``
    * - ``logging_config_file``
      - The configuration file name specified in logging package
      - ``logging.conf``
    * - ``logging_logger_name``
      - The logger name when using the logging package
      - ``debugtrace``
    * - ``logging_level``
      - | The log level when using the logging package
        |
        | Specifiable Values:
        | ``CRITICAL``
        | ``ERROR``
        | ``WARNING``
        | ``INFO``
        | ``DEBUG``
        | ``NOTSET``
      - ``DEBUG``
    * - ``is_enabled``
      - | Specifiable Values:
        | ``False: Log output is disabled``
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
    * - ``thread_boundary_format``
      - | The format string of logging at threads boundary
        | ``{0}: The thread name``
        | ``{1}: The thread ID``
      - ``______________________________ {0} #{1} ______________________________``
    * - ``maximum_indents``
      - The maximum number of indents
      - ``32``
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
      - | ``16`` *(since 1.2.0)*
        | ``5`` *(until 1.1.0)*
    * - ``length_format``
      - The format string of the length of string and ``bytes``
      - ``length:{}``
    * - ``minimum_output_length``
      - The minimum value to output the length of string and ``bytes``
      - | ``16`` *(since 1.2.0)*
        | ``5`` *(until 1.1.0)*
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
      - | ``128`` *(since 1.2.0)*
        | ``512`` *(until 1.1.0)*
    * - ``bytes_limit``
      - The limit value of elements for ``bytes`` and ``bytearray``  to output
      - | ``256`` *(since 1.2.0)*
        | ``8192`` *(until 1.1.0)*
    * - ``string_limit``
      - The limit value of characters for string to output
      - | ``256`` *(since 1.2.0)*
        | ``8192`` *(until 1.1.0)*
    * - ``reflection_nest_limit``
      - The The limit value for reflection nesting
      - ``4``

*Converts* ``\s`` *to space.*

6. License
==========

MIT License (MIT)

7. Release notes
================

``DebugTrace-py 1.2.0 - August 15, 2022``
-----------------------------------------

* Added the runtime Python version to the startup log.
* Changed to output a log that shows thread switching.
* Changed default values for the following properties.

.. list-table::
    :widths: 17, 12, 12
    :header-rows: 1

    * - Property Name
      - New Default Value
      - Old Default Value
    * - minimum_output_count
      - 16
      - 5
    * - minimum_output_length
      - 16
      - 5
    * - collection_limit
      - 128
      - 512
    * - string_limit
      - 256
      - 8192
    * - bytes_limit
      - 256
      - 8192

``DebugTrace-py 1.1.0 - November 28, 2021``
-------------------------------------------

* Fixed a bug that an error occurs when outputting an object of a class that implements ``__str__`` or ``__repr__``. 
* Do not output ``tuple``, ``set``, ``dict`` data types.
    | ``(1, 2, 3)`` ← ``(tuple)(1, 2, 3)``
    | ``(1,)`` ← ``(tuple)(1)``
    | ``()`` ← ``(tuple)()``
    | ``{1, 2, 3}`` ← ``(set){1, 2, 3}``
    | ``{}`` ← ``(set){}``
    | ``{1: 'A', 2: 'B', 3; 'C'}`` ← ``(dict){1: 'A', 2: 'B', 3; 'C'}``
    | ``{:}`` ← ``(dict){}``

``DebugTrace-py 1.0.3 - August 12, 2021``
-------------------------------------------

* Improved the line break handling of data output

``DebugTrace-py 1.0.2 - November 29, 2020``
-------------------------------------------

* Change the start message. (``'DebugTrace-py ...'`` <- ``'DebugTrace-python ...'``)

``DebugTrace-py 1.0.1 - July 19, 2020``
-------------------------------------------

* Improved the line break handling of data output.

``DebugTrace-py 1.0.0 - May 26, 2020``
-------------------------------------------

* First release

*(C) 2020 Masato Kokubo*
