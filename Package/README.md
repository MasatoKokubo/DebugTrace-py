# DebugTrace-py

**DebugTrace-py** is a library that outputs trace logs
when debugging your Python programs.
It supports Python 3.7 or later.
By embedding "`_ = debugtrace.enter()`" at the start of the method,
you can output the execution status of the program under development.

## 1. Features

* Automatically outputs the method name, source file name and line number
  of invokers of `debugtrace.enter` function.
* Also outputs end logs when the scope ends.
* Indents logs automatically with nested methods and objects.
* Automatically line breaks in value output.
* Uses reflection to output content even for objects of classes
  that do not implement the `__str__` method.
* You can customize output contents by setting `debugtrace.ini` file.
* You can select sys.stdout, sys.stderr or logging.Logger to output.

## 2. Install

`pip install debugtrace`

## 3. How to use

Do the following for the debug target and related functions and methods:

* Insert "`_ = debugtrace.enter()`" at the beginning of functions and methods.
* Insert "`debugtrace.print('foo', foo)`" to output variables to the log if necessary.

The following is an example of a Python program using DebugTrace-py and a log when it is executed.

```python:readme_example.py
  # readme_example.py
  import datetime
  import debugtrace

  # Contact class
  class Contact(object):
      def __init__(self, id: int, firstName: str, lastName: str, birthday: datetime.date) -> None:
          _ = debugtrace.enter(self)
          self.id = id
          self.firstName = firstName
          self.lastName  = lastName
          self.birthday  = birthday

  def func2():
      _ = debugtrace.enter()
      contact = [
          Contact(1, 'Akane' , 'Apple', datetime.date(1991, 2, 3)),
          Contact(2, 'Yukari', 'Apple', datetime.date(1992, 3, 4))
      ]
      debugtrace.print('contact', contact)

  def func1():
      _ = debugtrace.enter()
      debugtrace.print('Hello, World!')
      func2()

  func1()
```

Log output contents:
```log
2024-03-29 18:43:38.112156+0900 DebugTrace-py 1.4.0 on Python 3.12.0
2024-03-29 18:43:38.112209+0900   config file path: <No config file>
2024-03-29 18:43:38.112244+0900   logger: sys.stderr
2024-03-29 18:43:38.112329+0900 
2024-03-29 18:43:38.112367+0900 ______________________________ MainThread #134705475060800 ______________________________
2024-03-29 18:43:38.112384+0900 
2024-03-29 18:43:38.113719+0900 Enter func1 (readme_example.py:22) <- (readme_example.py:26)
2024-03-29 18:43:38.113813+0900 | Hello, World! (readme_example.py:23)
2024-03-29 18:43:38.113907+0900 | Enter func2 (readme_example.py:14) <- (readme_example.py:24)
2024-03-29 18:43:38.114001+0900 | | Enter Contact.__init__ (readme_example.py:7) <- (readme_example.py:16)
2024-03-29 18:43:38.114074+0900 | | Leave Contact.__init__ (readme_example.py:7) duration: 0:00:00.000008
2024-03-29 18:43:38.114166+0900 | | 
2024-03-29 18:43:38.114202+0900 | | Enter Contact.__init__ (readme_example.py:7) <- (readme_example.py:17)
2024-03-29 18:43:38.114240+0900 | | Leave Contact.__init__ (readme_example.py:7) duration: 0:00:00.000007
2024-03-29 18:43:38.114534+0900 | | 
2024-03-29 18:43:38.114574+0900 | | contacts = [
2024-03-29 18:43:38.114596+0900 | |   (__main__.Contact){
2024-03-29 18:43:38.114609+0900 | |     birthday: 1991-02-03, firstName: 'Akane', id: 1, lastName: 'Apple'
2024-03-29 18:43:38.114646+0900 | |   },
2024-03-29 18:43:38.114703+0900 | |   (__main__.Contact){
2024-03-29 18:43:38.114727+0900 | |     birthday: 1992-03-04, firstName: 'Yukari', id: 2, lastName: 'Apple'
2024-03-29 18:43:38.114738+0900 | |   }
2024-03-29 18:43:38.114748+0900 | | ] (readme_example.py:19)
2024-03-29 18:43:38.114778+0900 | | 
2024-03-29 18:43:38.114818+0900 | Leave func2 (readme_example.py:14) duration: 0:00:00.000863
2024-03-29 18:43:38.114859+0900 Leave func1 (readme_example.py:22) duration: 0:00:00.001086
```

## 4. Functions

There are mainly the following functions.

<table>
    <caption>Function list<caption>
    <tr><th>Name</th><th>Discription</th></tr>
    <tr>
        <td><code>enter</code></td>
        <td>
            Outputs an entering log<br>
            Also outputs a leaving log at the end of the code block.<br>
            <br>
            <i>Arguments:</i><br>
            <ul>
                <code><b>invoker</b> (object, optional)</code>: Pass the <code>self</code> or <code>cls</code> of the invoker.
            </ul>
            <i>Examples:</i><br>
            <ul>
                <code>   _ = debugtrace.enter(self)<br>
    _ = debugtrace.enter(cls)<br>
    _ = debugtrace.enter()</code>
            </ul>
        </td>
    </tr>
    <tr>
        <td><code>print</code></td>
        <td>
            Outputs the variable name and value<br>
            <br>
            <i>Arguments:</i><br>
            <code><b>name</b> (str)</code>: Variable name, etc<br>
            <code><b>value</b> (object, optional)</code>: Value to output (output only name if omitted)<br>
            <br>
            The following are keyword arguments<br>
            <br>
            <code><b>force_reflection</b> (bool, optional)</code>: If <code>True</code>, outputs using reflection even if it has a <code>__str__</code> or <code>__repr__</code> method (default: <code>False</code>)<br>
            <code><b>output_private</b> (bool, optional)</code>: If <code>True</code>, also outputs private members when using reflection (default: <code>False</code>)<br>
            <code><b>output_method</b> (bool, optional)</code>: If <code>True</code>, also outputs method members when using reflection (default: <code>False</code>)<br>
            <code><b>collection_limit</b> (int, optional)</code>: The limit value of elements such as <code>list</code>, <code>tuple</code> and <code>dict</code> to output (default: <code>-1</code>)<br>
            <code><b>bytes_limit</b> (int, optional)</code>: The limit value of elements for <code>bytes</code> and <code>bytearray</code> to output (default: <code>-1</code>)<br>
            <code><b>string_limit</b> (int, optional)</code>: The limit value of characters for string to output (default: <code>-1</code>)<br>
            <code><b>reflection_nest_limit</b> (int, optional)</code>: The The limit value for reflection nesting (default: <code>-1</code>)<br>
            <br>
            <i>Examples:</i><br>
            <code>   debugtrace.print('Hellow')<br>
    debugtrace.print('foo', foo)<br>
    debugtrace.print('foo', foo, force_reflection=<code>True</code>)<br>
    debugtrace.print('foos', foos, collection_limit=1024)</code>
        </td>
    </tr>
</table>

## 5. Options that can be specified in the **debugtrace.ini** file

DebugTrace-py reads the `debugtrace.ini` file
in the current directory for initialization.
The section is `[debugtrace]`.

You can specify the following options in the `debugtrace.ini` file.

<table>
    <caption>debugtrace.ini<caption>
    <tr><th>Option Name</th><th>Description</th><th>Default Value</th></tr>
    <tr>
        <td><code>logger</code></td>
        <td>
            The logger used by debugtrace<br>
            Specifiable Values:<br>
            <code>stdout</code> - Output to <code>sys.stdout</code><br>
            <code>stderr</code> - Output to <code>sys.stderr</code><br>
            <code>logger</code> - Output using <code>logging</code> package<br>
            <code>file:</code>< log file path> - Output directly to the file
        </td>
        <td><code>stderr</code></td>
    </tr>
    <tr>
        <td><code>logging_config_file</code></td>
        <td>The configuration file name specified in logging package</td>
        <td><code>logging.conf</code></td>
    </tr>
    <tr>
        <td><code>logging_logger_name</code></td>
        <td>The logger name when using the logging package</td>
        <td><code>debugtrace</code></td>
    </tr>
    <tr>
        <td><code>is_enabled</code></td>
        <td>
            Specifiable Values:<br>
           <code>False</code>: Log output is disabled<br>
           <code>True</code>: Log output is enabled
        </td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td><code>enter_format</code></td>
        <td>
            The format string of log output when entering functions or methods<br>
            <code>{0}</code>: The function or method name<br>
            <code>{1}</code>: The file name<br>
            <code>{2}</code>: The line number<br>
            <code>{3}</code>: The file name of the caller<br>
            <code>{4}</code>: The line number of the caller
        </td>
        <td><code>Enter {0} ({1}:{2}) <- ({3}:{4})</code></td>
    </tr>
    <tr>
        <td><code>leave_format</code></td>
        <td>
            The format string of log output when leaving functions or methods<br>
            <code>{0}</code>: The function or method name<br>
            <code>{1}</code>: The file name<br>
            <code>{2}</code>: The line number<br>
            <code>{3}</code>: The time since entered
        </td>
        <td><code>Leave {0} ({1}:{2}) duration: {3}</code></td>
    </tr>
    <tr>
        <td><code>thread_boundary_format</code></td>
        <td>
            The format string of logging at threads boundary<br>
            <code>{0}</code>: The thread name<br>
            <code>{1}</code>: The thread ID
        </td>
        <td>
            <code>______________________________ {0} #{1} ______________________________</code>
        </td>
    </tr>
    <tr>
        <td><code>maximum_indents</code></td>
        <td>イThe maximum number of indents</td>
        <td>32</td>
    </tr>
    <tr>
        <td><code>indent_string</code></td>
        <td>The indentation string for code</td>
        <td><code>\s</code></td>
    </tr>
    <tr>
        <td><code>data_indent_string</code></td>
        <td>The indentation string for data</td>
        <td><code>\s\s<code></td>
    </tr>
    <tr>
        <td><code>limit_string<code></td>list
        <td>The string to represent that it has exceeded the limit</td>
        <td><code>...</code></td>
    </tr>
    <tr>
        <td><code>non_output_string</code><br>(Currently unused)</td>
        <td>The string to be output instead of not outputting value</td>
        <td><code>...</code></td>
    </tr>
    <tr>
        <td><code>cyclic_reference_string</code></td>
        <td>The string to represent that the cyclic reference occurs</td>
        <td><code>*** Cyclic Reference ***</code></td>
    </tr>
    <tr>
        <td><code>varname_value_separator</code></td>
        <td>The separator string between the variable name and value</td>
        <td><code>\s=\s</code></td>
    </tr>
    <tr>
        <td><code>key_value_separator</code></td>
        <td>The separator string between the key and value of dictionary and between the attribute name and value</td>
        <td><code>:\s</code></td>
    </tr>
    <tr>
        <td><code>print_suffix_format<c/ode></td>
        <td>The format string of <code>print</code> method suffix</td>
        <td><code>\s({1}:{2})</code></td>
    </tr>
    <tr>
        <td><code>count_format</code></td>
        <td>
            The format string of the number of elements for <code>list</code>, <code>tuple</code> and <code>dict</code>
        </td>
        <td><code>count:{}</code></td>
    </tr>
    <tr>
        <td><code>minimum_output_count</code></td>
        <td>
            The minimum value to output the number of elements for <code>list</code>, <code>tuple</code> and <code>dict</code>
        </td>
        <td>128</td>
    </tr>
    <tr>
        <td><code>length_format</code></td>
        <td>The format string of the length of string and <code>bytes</code></td>
        <td><code>length:{}</code></td>
    </tr>
    <tr>
        <td><code>minimum_output_length</code></td>
        <td>The minimum value to output the length of string and <code>bytes</code></td>
        <td>256</td>
    </tr>
    <tr>
        <td><code>log_datetime_format</code></td>
        <td>Log date and time format when <code>logger</code> is <code>StdOut</code> or <code>StdErr</code></td>
        <td><code>%Y-%m-%d %H:%M:%S.%f%z</code></td>
    </tr>
    <tr>
        <td><code>maximum_data_output_width</code></td>
        <td>The maximum output width of data</td>
        <td>70</td>
    </tr>
    <tr>
        <td><code>bytes_count_in_line</code></td>
        <td>The count in line of <code>bytes</code></td>
        <td>16</td>
    </tr>
    <tr>
        <td><code>collection_limit</code></td>
        <td>
            The limit value of elements for <code>list</code>, <code>tuple</code> and <code>dict</code> to output
        </td>
        <td>128</td>
    </tr>
    <tr>
        <td><code>bytes_limit</code></td>
        <td>The limit value of elements for <code>bytes</code> and <code>bytearray</code> to output</td>
        <td>256</td>
    </tr>
    <tr>
        <td><code>string_limit</code></td>
        <td>The limit value of characters for string to output</td>
        <td>256</td>
    </tr>
    <tr>
        <td><code>reflection_nest_limit</code></td>
        <td>The The limit value for reflection nesting</td>
        <td>4</td>
    </tr>
</table>

*Converts* `\s` *to space.*

## 6. License

[MIT License (MIT)](LICENSE)

*&copy; 2020 Masato Kokubo*

## 7. Release notes

### DebugTrace-py 1.4.0 - March 31, 2024

* `print` method now returns the `value` of the argument.
* Changed default values for the following properties.

|Property Name|New Default Value|Old Default Value|
|:------------|:---------------:|:---------------:|
|minimum_output_count |128|16|
|minimum_output_length|256|16|

### DebugTrace-py 1.3.0 - March 4, 2023

* Added calling source file name and line number to log output of `enter` method.
* Abolished `logging_level` setting in `debugtrace.ini` and set it to fixed (`DEBUG`).
* Added `log_datetime_format` to `debugtrace.ini` setting item.

### DebugTrace-py 1.2.0 - August 15, 2022

* Added the runtime Python version to the startup log.
* Changed to output a log that shows thread switching.
* Changed default values for the following properties.

|Property Name|New Default Value|Old Default Value|
|:------------|:---------------:|:---------------:|
|minimum_output_count | 16|   5|
|minimum_output_length| 16|   5|
|collection_limit     |128| 512|
|bytes_limit          |256|8192|
|string_limit         |256|8192|

### DebugTrace-py 1.1.0 - November 28, 2021

* Fixed a bug that an error occurs when outputting an object of a class that implements `__str__` or `__repr__`. 
* Do not output `tuple`, `set`, `dict` data types.
    `(1, 2, 3)` ← `(tuple)(1, 2, 3)`  
    `(1,)` ← `(tuple)(1)`  
    `()` ← `(tuple)()`  
    `{1, 2, 3}` ← `(set){1, 2, 3}`  
    `{}` ← `(set){}`  
    `{1: 'A', 2: 'B', 3; 'C'}` ← `(dict){1: 'A', 2: 'B', 3; 'C'}`  
    `{:}` ← `(dict){}`  

### DebugTrace-py 1.0.3 - August 12, 2021

* Improved the line break handling of data output

### DebugTrace-py 1.0.2 - November 29, 2020

* Change the start message. (`'DebugTrace-py ...'` <- `'DebugTrace-python ...'`)

### DebugTrace-py 1.0.1 - July 19, 2020

* Improved the line break handling of data output.

### DebugTrace-py 1.0.0 - May 26, 2020

* First release
