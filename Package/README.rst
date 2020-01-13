#################
DebugTrace-python
#################

**DebugTrace-python** is a library that outputs trace logs
when debugging your Python programs.
It supports Python 3.5 or later.
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
* Insert "``debugtrace.print_('foo', foo)``" to output variables to the log if necessary.

The following is an example of a Python program using DebugTrace-python and a log when it is executed.

::

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
        debugtrace.print_("contact", contact) # for Debugging

    def func1():
        _ = debugtrace.enter() # for Debugging
        func2()

    func1()

Log output contents:
::

    2020-01-13 11:38:02.421897 debugtrace 1.0.0b1 logger: StdErr
    2020-01-13 11:38:02.424168 Enter func1 (ReadmeExample.py:32)
    2020-01-13 11:38:02.424248 |   Enter func2 (ReadmeExample.py:24)
    2020-01-13 11:38:02.424727 |   |   contact = (list)[
    2020-01-13 11:38:02.424743 |   |     (__main__.Contact){
    2020-01-13 11:38:02.424750 |   |       birthday: 1991-02-03,
    2020-01-13 11:38:02.424756 |   |       firstName: (length:5)'Akane',
    2020-01-13 11:38:02.424761 |   |       id: 1,
    2020-01-13 11:38:02.424766 |   |       lastName: (length:5)'Apple',
    2020-01-13 11:38:02.424771 |   |     },
    2020-01-13 11:38:02.424777 |   |     (__main__.Contact){
    2020-01-13 11:38:02.424782 |   |       birthday: 1992-03-04,
    2020-01-13 11:38:02.424787 |   |       firstName: (length:6)'Yukari',
    2020-01-13 11:38:02.424798 |   |       id: 2,
    2020-01-13 11:38:02.424804 |   |       lastName: (length:5)'Apple',
    2020-01-13 11:38:02.424809 |   |     },
    2020-01-13 11:38:02.424814 |   |   ]
    2020-01-13 11:38:02.424824 |   Leave func2
    2020-01-13 11:38:02.424833 Leave func1


4. Functions
============

There are mainly the following functions.

.. list-table:: Function list
    :widths: 10, 20, 70
    :header-rows: 1

    * - Name
      - Arguments
      - Discription
    * - ``enter``
      - None
      - | Outputs an entering log.
        | Also outputs a leaving log at the end of the code block.
        | *Example*:
        | ``_ = debugtrace.enter()``
    * - ``print_``
      - | ``name``: Variable name, etc.
        | ``value``: Output value
      - | Outputs the variable name and value.
        | *Example*:
        | ``debugtrace.print_('foo', foo)```


5. Options that can be specified in the **debugtrace.ini** file
===============================================================

DebugTrace-python reads the `` debugtrace.ini`` file
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
    * - ``enter_string``
      - String to be output when entering functions and methods
      - ``Enter``
    * - ``leave_string``
      - String to output when leaving functions and methods
      - ``Leave``
    * - ``limit_string``
      - String output when limit is exceeded
      - ``...``
    * - ``maximum_indents``
      - Maximum number of indents
      - ``20``
    * - ``code_indent_string``
      - Indentation string for code
      - ｜␠␠␠
    * - ``data_indent_string``
      - Indentation string for data
      - | ␠␠
        | (2 spaces)
    * - ``non_output_string``
      - String to be output instead of not outputting value
      - ``...``
    * - ``cyclic_reference_string``
      - String to be output when referring to a cycle
      - ``*** Cyclic Reference ***``
    * - ``varname_value_separator``
      - String separating variable name and value
      - ``␠=␠``
    * - ``key_value_separator``
      - | String separating the dictionary key and value
        | And separating the attribute name and value
      - ``:␠``
    * - ``log_datetime_format``
      - Log date and time format when ``logger`` is ``StdOut`` or ``StdErr``
      - ``%Y-%m-%d %H:%M:%S.%f``
    * - ``enter_format``
      - | Format of the log output when entering function or method
        | ``{0}: function or method name``
        | ``{1}: file name``
        | ``{2}: line number``
      - ``{0} ({1}:{2})``
    * - ``leave_format``
      - | Format of log output when leaving function or method
        | ``{0}: function or method name``
      - ``{0}``
    * - ``count_format``
      - Output format of the number of elements such as ``list``, ``tuple``, ``dict`` and etc.
      - ``count:{}``
    * - ``minimum_output_count``
      - Minimum value to output the number of elements such as ``list``, ``tuple``, ``dict`` and etc.
      - ``5``
    * - ``string_length_format``
      - Output format for string length
      - ``length:{}``
    * - ``minimum_output_string_length``
      - Minimum value to output string length
      - ``5``
    * - ``maximum_data_output_width``
      - Maximum output width of data
      - ``80``
    * - ``collection_limit``
      - Maximum number of elements to output such as ``list``, ``tuple``, ``dict`` and etc.
      - ``256``
    * - ``string_limit``
      - Maximum number of output characters for string values
      - ``2048``
    * - ``reflection_nest_limit``
      - Maximum number of reflection nests
      - ``4``

6. License
==========

MIT License (MIT)

7. Release notes
================

``DebugTrace-python 1.0.0b1 - 2020-01-13``
------------------------------------------

* First release (beta version)

*(C) 2020 Masato Kokubo*
