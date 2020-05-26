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
  of callers of ``debugtrace.enter`` function.
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

Do the following for the debuggee and related functions or methods:

* Insert "``_ = debugtrace.enter()``" at the beginning of functions and methods.
* Insert "``debugtrace.print('foo', foo)``" to output variables to the log if necessary.

The following is an example of a Python program using DebugTrace-python and a log when it is executed.

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

    2020-05-25 23:40:36.825030 DebugTrace-python 1.0.0
    2020-05-25 23:40:36.825094 　logger: sys.stderr
    2020-05-25 23:40:36.825125   config file path: <No config file>
    2020-05-25 23:40:36.825150 
    2020-05-25 23:40:36.828820 Enter func1 (ReadmeExample.py:23)
    2020-05-25 23:40:36.828983 | Enter func2 (ReadmeExample.py:15)
    2020-05-25 23:40:36.829047 | | Enter Contact.__init__ (ReadmeExample.py:8)
    2020-05-25 23:40:36.829119 | | Leave Contact.__init__ (ReadmeExample.py:8) duration: 0:00:00.000014
    2020-05-25 23:40:36.829196 | | 
    2020-05-25 23:40:36.829235 | | Enter Contact.__init__ (ReadmeExample.py:8)
    2020-05-25 23:40:36.829279 | | Leave Contact.__init__ (ReadmeExample.py:8) duration: 0:00:00.000004
    2020-05-25 23:40:36.829808 | | 
    2020-05-25 23:40:36.829849 | | contact = (list)[
    2020-05-25 23:40:36.829881 | |   (__main__.Contact){
    2020-05-25 23:40:36.829920 | |     birthday: 1991-02-03, firstName: (length:5)'Akane', id: 1, lastName:
    2020-05-25 23:40:36.829946 | |     (length:5)'Apple'
    2020-05-25 23:40:36.829972 | |   },
    2020-05-25 23:40:36.829997 | |   (__main__.Contact){
    2020-05-25 23:40:36.830022 | |     birthday: 1992-03-04, firstName: (length:6)'Yukari', id: 2, lastName:
    2020-05-25 23:40:36.830048 | |     (length:5)'Apple'
    2020-05-25 23:40:36.830073 | |   }
    2020-05-25 23:40:36.830098 | | ] (ReadmeExample.py:20)
    2020-05-25 23:40:36.830128 | | 
    2020-05-25 23:40:36.830163 | Leave func2 (ReadmeExample.py:15) duration: 0:00:00.001125
    2020-05-25 23:40:36.830202 Leave func1 (ReadmeExample.py:23) duration: 0:00:00.001310

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
        | **collection_limit** (``int``): Limit value of elements such as ``list``, ``tuple`` and ``dict`` to output (default: ``None``)
        | **bytes_limit** (``int``):  Limit value of elements for ``bytes`` and ``bytearray`` to output (default: ``None``)
        | **string_limit** (``int``): Limit value of characters for string to output (default: ``None``)
        | **reflection_nest_limit** (int): Limit value of reflection nests (default: ``None``)
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
      - | Logger used by debugtrace
        | ``StdOut: Output to sys.stdout``
        | ``StdErr: Output to sys.stderr``
        | ``Logger: Output using logging package``
      - ``StdErr``
    * - ``logging_config_file``
      - Configuration file name specified in logging package
      - ``logging.conf``
    * - ``logging_logger_name``
      - Logger name when using the logging package
      - ``debugtrace``
    * - ``logging_level``
      - Log level when using the logging package
      - ``DEBUG``
    * - ``is_enabled``
      - | ``False: Log output is disabled``
        | ``True: Log output is enabled``
      - ``True``
    * - ``enter_format``
      - | Format string of log output when entering functions or methods
        | ``{0}: The function or method name``
        | ``{1}: The file name``
        | ``{2}: The line number``
      - ``Enter {0} ({1}:{2})``
    * - ``leave_format``
      - | Format string of log output when leaving functions or methods
        | ``{0}: The function or method name``
        | ``{1}: The file name``
        | ``{2}: The line number``
        | ``{3}: The time from entering``
      - ``Leave {0} ({1}:{2}) duration: {3}``
    * - ``maximum_indents``
      - Maximum number of indents
      - ``20``
    * - ``indent_string``
      - Indentation string for code
      - ``|\s``
    * - ``data_indent_string``
      - Indentation string for data
      - ``\s\s``
    * - ``limit_string``
      - String to represent that it has exceeded the limit
      - ``...``
    * - ``non_output_string``
      - | String to be output instead of not outputting value
        | (Currently unused)
      - ``...``
    * - ``cyclic_reference_string``
      - String to represent that the cyclic reference occurs
      - ``*** Cyclic Reference ***``
    * - ``varname_value_separator``
      - Separator string between the variable name and value
      - ``\s=\s``
    * - ``key_value_separator``
      - Separator string between the key and value of dictionary and between the attribute name and value
      - ``:\s``
    * - ``print_suffix_format``
      - Format string of ``print`` method suffix
      - ``\s({1}:{2})``
    * - ``count_format``
      - Format string of the number of elements such as ``list``, ``tuple`` and ``dict``
      - ``count:{}``
    * - ``minimum_output_count``
      - Minimum value to output the number of elements such as ``list``, ``tuple`` and ``dict``
      - ``5``
    * - ``length_format``
      - Format string of the length of string and ``bytes``
      - ``length:{}``
    * - ``minimum_output_length``
      - Minimum value to output the length of string and ``bytes``
      - ``5``
    * - ``log_datetime_format``
      - | Log date and time format when ``logger`` is ``StdOut`` or ``StdErr``
        | (Currently not configurable)
      - ``%Y-%m-%d %H:%M:%S.%f``
    * - ``maximum_data_output_width``
      - Maximum output width of data
      - ``70``
    * - ``bytes_count_in_line``
      - Count in line of ``bytes``
      - ``16``
    * - ``collection_limit``
      - Limit value of elements such as ``list``, ``tuple`` and ``dict`` to output
      - ``512``
    * - ``bytes_limit``
      - Limit value of elements for ``bytes`` and ``bytearray``  to output
      - ``8192``
    * - ``string_limit``
      - Limit value of characters for string to output
      - ``8192``
    * - ``reflection_nest_limit``
      - Limit value of reflection nests
      - ``4``

*Converts* ``\s`` *to space.*

6. License
==========

MIT License (MIT)

7. Release notes
================

``DebugTrace-python 1.0.0 - May. 26, 2020``
------------------------------------------------

 First release

*(C) 2020 Masato Kokubo*
