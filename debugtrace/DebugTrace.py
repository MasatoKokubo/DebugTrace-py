# DebugTrace.py
# (C) 2020 Masato Kokubo
import os
import configparser
import inspect
import traceback
import datetime

class Config(object):
    __CONFIG_PATH    = './debugtrace.ini'
    __CONFIG_SECTION = 'debugtrace'

    config = configparser.ConfigParser()
    if os.path.exists(__CONFIG_PATH):
        config.read(__CONFIG_PATH)

    @classmethod
    def get_value(cls, key: str, fallback: object) -> object:
        value = fallback
        try:
            if cls.config == None:
                cls.config = configparser.ConfigParser()
                cls.config.read(cls.__CONFIG_PATH)

            if type(fallback) == bool:
                value = cls.config.getboolean(cls.__CONFIG_SECTION, key, fallback=fallback)
            elif type(fallback) == int:
                value = cls.config.getint(cls.__CONFIG_SECTION, key, fallback=fallback)
            else:
                value = cls.config.get(cls.__CONFIG_SECTION, key, fallback=fallback)
                value = value.replace('\\s', ' ')

        except BaseException as ex:
            print('Config.get_value: key: ' + key + ', error: '  + str(ex))

        return value

class DebugTrace(object):
    """Debug Trace class

    Class Attributes:
        is_enabled                  (bool): True if log output is enabled, False otherwise
        enter_string                 (str): Log string when entering blocks
        leave_string                 (str): Log string when leaving blocks
        maximum_indents              (int): Maximum number of indents
        code_indent_string           (str): A code indent string
        data_indent_string           (str): A data indent string
        limit_string                 (str): String to represent that it has exceeded the limit
        non_output_string            (str): String of value in the case of attributes that do not output the value
        cyclic_reference_string      (str): String to represent that the cyclic reference occurs
        varname_value_separator      (str): Separator string between the variable name and value
        key_value_separator          (str): Separator string between the key and value of dictionaries and attributes
        log_datetime_format          (str): Format string for Datetime
        enter_format                 (str): Format string when entering blocks
        leave_format                 (str): Format string when leaving blocks
        count_format                 (str): Format for the number of elements in lists, tuples, and dictionaries 
        minimum_output_count         (int): Minimum output count
        string_length_format         (str): Format for the length of strings
        minimum_output_string_length (int): Minimum output string length
        maximum_data_output_width    (int): Maximum output width of data
        collection_limit             (int): Limit value of list, tuple and dictionaly elements to output
        string_limit                 (int): Limit value of string characters to output
        reflection_nest_limit        (int): Limit value of reflection nest
        non_output_attributes       (list): (Not implemented) Attributes not to be output value
        reflection_classes          (list): (Not implemented) Classe names that output content by reflection even if __str__ method is implemented
        output_non_public_attributes(bool): (Not implemented) If True, outputs the contents by reflection even for fields which are not public
    """
#       log_time_zone  (datetime.timezone): Time zone of the date and time when outputting logs

    __DO_NOT_OUTPUT              = 'Do not output'

    is_enabled                   = Config.get_value('is_enabled'                  , True                      )
    enter_string                 = Config.get_value('enter_string'                , 'Enter'                   )
    leave_string                 = Config.get_value('leave_string'                , 'Leave'                   )
    limit_string                 = Config.get_value('limit_string'                , '...'                     )
    maximum_indents              = Config.get_value('maximum_indents'              , 20                       )
    code_indent_string           = Config.get_value('code_indent_string'          , '|   '                    )
    data_indent_string           = Config.get_value('data_indent_string'          , '  '                      )
    non_print_string             = Config.get_value('non_print_string'            , '...'                     )
    cyclic_reference_string      = Config.get_value('cyclic_reference_string'     , '*** Cyclic Reference ***')
    varname_value_separator      = Config.get_value('varname_value_separator'     , ' = '                     )
    key_value_separator          = Config.get_value('key_value_separator'         , ': '                      )
    log_datetime_format          = Config.get_value('log_datetime_format'         , '%Y-%m-%d %H:%M:%S.%f%z'  )
    enter_format                 = Config.get_value('enter_format'                , '{0} ({1}:{2})'           )
    leave_format                 = Config.get_value('leave_format'                , '{0}'                     )
    count_format                 = Config.get_value('count_format'                , 'count:{}'                )
    minimum_output_count         = Config.get_value('minimum_output_count'        , 5                         )
    string_length_format         = Config.get_value('string_length_format'        , 'length:{}'               )
    minimum_output_string_length = Config.get_value('minimum_output_string_length', 5                         )
    maximum_data_output_width    = Config.get_value('maximum_data_output_width'   , 80                        )
    collection_limit             = Config.get_value('collection_limit'            , 256                       )
    string_limit                 = Config.get_value('string_limit'                , 2048                      )
    reflection_nest_limit        = Config.get_value('reflection_nest_limit'       , 4                         )
    non_output_attributes        = [] # Not implemented
    reflection_classes           = [] # Not implemented
    output_non_public_attributes = [] # Not implemented
#   log_time_zone: datetime.timezone = None

    __slots__             = ['frame_summary']
    __code_indent_strings = []
    __data_indent_strings = []
    __code_nest_level     = 0
    __previous_nest_level = 0
    __data_nest_level     = 0
    __reflected_objects   = []
    
    def __init__(self):
        if not DebugTrace.is_enabled: return

        try:
            raise RuntimeError
        except RuntimeError:
            self.frame_summary = traceback.extract_stack(limit=2)[0]

        print(DebugTrace.__get_datetime_string() + ' ' +
            DebugTrace.__get_indent_string() +
            DebugTrace.enter_string + ' ' +
            DebugTrace.enter_format.format(
                self.frame_summary.name,
                os.path.basename(self.frame_summary.filename),
                self.frame_summary.lineno
            )
        )
        DebugTrace.__up_nest()

    def __del__(self):
        if not DebugTrace.is_enabled: return

        DebugTrace.__down_nest()
        print(DebugTrace.__get_datetime_string() + ' ' +
            DebugTrace.__get_indent_string() +
            DebugTrace.leave_string + ' ' +
            DebugTrace.leave_format.format(self.frame_summary.name)
        )


    @classmethod
    def __up_nest(cls) -> None:
        cls.__previous_nest_level = cls.__code_nest_level
        cls.__code_nest_level += 1

    @classmethod
    def __down_nest(cls) -> None:
        cls.__previous_nest_level = cls.__code_nest_level
        cls.__code_nest_level -= 1

    @classmethod
    def __get_datetime_string(cls) -> str:
    #   return datetime.datetime.now(cls.log_time_zone).strftime(cls.log_datetime_format)
        return datetime.datetime.now().strftime(cls.log_datetime_format)

    @classmethod
    def __get_indent_string(cls) -> str:
        if len(cls.__code_indent_strings) == 0:
            cls.__code_indent_strings = \
                [cls.code_indent_string * index for index in range(0, cls.maximum_indents)]

        return cls.__code_indent_strings[
            0 if (cls.__code_nest_level < 0) else
            len(cls.__code_indent_strings) - 1 if (cls.__code_nest_level >= len(cls.__code_indent_strings)) else
            cls.__code_nest_level
        ]

    @classmethod
    def __get_data_indent_string(cls) -> str:
        if len(cls.__data_indent_strings) == 0:
            cls.__data_indent_strings = \
                [cls.data_indent_string * index for index in range(0, cls.maximum_indents)]

        return cls.__data_indent_strings[
            0 if (cls.__data_nest_level < 0) else
            len(cls.__data_indent_strings) - 1 if (cls.__data_nest_level >= len(cls.__data_indent_strings)) else
            cls.__data_nest_level
        ]

    @classmethod
    def __to_strings(cls, value: object) -> list:
        strings = []
        if isinstance(value, type(None)):
            # None
            strings.append('None')
        elif isinstance(value, str):
            # str
            has_single_quote = False
            has_double_quote = False
            single_quote_str = \
                '(' + cls.string_length_format.format(len(value)) + ')' if len(value) >= cls.minimum_output_string_length \
                else ''
            double_quote_str = single_quote_str
            single_quote_str += "'"
            double_quote_str += '"'
            count = 1
            for char in value:
                if count > cls.string_limit:
                    single_quote_str += cls.limit_string
                    double_quote_str += cls.limit_string
                    break
                if char == "'":
                    single_quote_str += "\\'"
                    double_quote_str += char
                    has_single_quote = True
                elif char == '"':
                    single_quote_str += char
                    double_quote_str += '\\"'
                    has_double_quote = True
                elif char == '\\':
                    single_quote_str += '\\\\'
                    double_quote_str += '\\\\'
                elif char == '\n':
                    single_quote_str += '\\n'
                    double_quote_str += '\\n'
                elif char == '\r':
                    single_quote_str += '\\r'
                    double_quote_str += '\\r'
                elif char == '\t':
                    single_quote_str += '\\t'
                    double_quote_str += '\\t'
                elif char < ' ':
                    num_str = format(ord(char), '02X')
                    single_quote_str += '\\x' + num_str
                    double_quote_str += '\\x' + num_str
                else:
                    single_quote_str += char
                    double_quote_str += char
                count += 1

            double_quote_str += '"'
            single_quote_str += "'"
            if has_single_quote and not has_double_quote:
                strings.append(double_quote_str)
            else:
                strings.append(single_quote_str)

        elif isinstance(value, int) or isinstance(value, float) or \
            isinstance(value, datetime.date) or isinstance(value, datetime.time) or \
            isinstance(value, datetime.datetime):
            # int, float, datetime.date, datetime.time, datetime.datetime
            strings.append(str(value))

        elif isinstance(value, list) or \
                isinstance(value, set) or isinstance(value, frozenset) or \
                isinstance(value, tuple) or \
                isinstance(value, dict):
            # list, set, frozenset, tuple, dict
            strings = cls.__to_strings_iter(value)

        elif cls.__has_str_method(value):
            # has __str__ method
            strings.append(str(value))

        else:
            # use refrection
            if any(map(lambda obj: value is obj, cls.__reflected_objects)):
                # cyclic reference
                strings.append(cls.cyclic_reference_string)
            elif len(cls.__reflected_objects) > cls.reflection_nest_limit:
                # over reflection level limitation
                strings.append(cls.limit_string)
            else:
                cls.__reflected_objects.append(value)
                strings = cls.__to_strings_using_refrection(value)
                cls.__reflected_objects.pop()

        return strings

    @classmethod
    def __to_strings_using_refrection(cls, value: object) -> list:
        strings = []
        members = inspect.getmembers(value,
            lambda v: not inspect.isclass(v) and not inspect.ismethod(v) and not inspect.isbuiltin(v))

        # try one line
        one_line = True
        string = cls.__get_type_name(value) + '{'
        delimiter = ''
        for member in members:
            name = member[0]
            if name.startswith('__') and name.endswith('__'):
                continue
            value_strings = cls.__to_strings(member[1])
            if len(value_strings) > 1:
                # value is not one line
                one_line = False
                break

            string += delimiter + name + cls.key_value_separator + value_strings[0]
            if len(string) > cls.maximum_data_output_width:
                one_line = False
                break

            delimiter = ', '
        
        if one_line:
            # strings is one line
            string += '}'
            strings.append(string)
        else:
            # strings is not one line
            strings.append(cls.__get_type_name(value) + '{')
            cls.__data_nest_level += 1
            data_indent_string = cls.__get_data_indent_string()

            for member in members:
                name = member[0]
                if name.startswith('__') and name.endswith('__'):
                    continue
                strings.append(data_indent_string + name + cls.key_value_separator)

                value_strings = cls.__to_strings(member[1])
                is_first = True
                for value_string in value_strings:
                    if is_first:
                        strings[-1] += value_strings[0]
                    else:
                        strings.append(value_string)
                    is_first = False

            cls.__data_nest_level -= 1
            strings.append(cls.__get_data_indent_string() + '}')

        return strings

    @classmethod
    def __to_strings_iter(cls, values: object) -> list:
        strings = []
        open_char = '{' # set, frozenset, dict
        close_char = '}'
        if isinstance(values, list):
            # list
            open_char = '['
            close_char = ']'
        elif isinstance(values, tuple):
            # tuple
            open_char = '('
            close_char = ')'
        
        # try one line
        one_line = True
        type_str = cls.__get_type_name(values, len(values))
        string = type_str
        string += open_char
        delimiter = ''
        count = 1
        for value in values:
            string += delimiter
            if count > cls.collection_limit:
                string += cls.limit_string
                break
            if isinstance(values, dict):
                # dictionary
                key_strings = cls.__to_strings(value)
                value_strings = cls.__to_strings(values[value])
                if len(key_strings) > 1 or len(value_strings) > 1:
                    # multi lines
                    one_line = False
                    break
                string += key_strings[0]
                string += cls.key_value_separator
                string += value_strings[0]
            else:
                # list, set, frozenset or tuple
                value_strings = cls.__to_strings(value)
                if len(value_strings) > 1:
                    # multi lines
                    one_line = False
                    break
                string += value_strings[0]

            if len(string) > cls.maximum_data_output_width:
                one_line = False
                break

            delimiter = ', '
            count += 1

        if one_line:
            # strings is one line
            string += close_char
            strings.append(string)

        else:
            # strings is not one line
            strings.append(type_str + open_char)
            cls.__data_nest_level += 1
            data_indent_string = cls.__get_data_indent_string()
            count = 1
            for value in values:
                if count > cls.collection_limit:
                    strings.append(data_indent_string + cls.limit_string)
                    break
                if isinstance(values, dict):
                    # dictionary
                    # key
                    key_strings = cls.__to_strings(value)
                    is_first = True
                    for key_string in key_strings:
                        if is_first:
                            strings.append(data_indent_string + key_string)
                        else:
                            strings.append(key_string)
                        is_first = False
                    strings[-1] += cls.key_value_separator

                    # value
                    value_strings = cls.__to_strings(values[value])
                    is_first = True
                    for value_string in value_strings:
                        if is_first:
                            strings[-1] += value_string
                        else:
                            strings.append(value_string)
                        is_first = False
                else:
                    # list, set or tuple
                    value_strings = cls.__to_strings(value)
                    is_first = True
                    for value_string in value_strings:
                        if is_first:
                            strings.append(data_indent_string + value_string)
                        else:
                            strings.append(value_string)
                        is_first = False

                strings[-1] += ','
                count += 1

            cls.__data_nest_level -= 1
            strings.append(cls.__get_data_indent_string() + close_char)

        return strings

    @classmethod
    def __get_type_name(cls, value: object, count: int = -1) -> str:
        type_name = str(type(value))
        if type_name.startswith("<class '"):
            type_name = type_name[8:]
        elif type_name.startswith("<enum '"):
            type_name = 'enum ' + type_name[7:]
        if type_name.endswith("'>"):
            type_name = type_name[:-2]
        return '(' + type_name + ')' if count < cls.minimum_output_count \
            else '(' + type_name + ' ' + cls.count_format.format(count) + ')'

    @classmethod
    def __has_str_method(cls, value: object) -> bool:
        members = inspect.getmembers(value, lambda v: inspect.ismethod(v))
        return len([member for member in members if member[0] == '__str__']) != 0

    @classmethod
    def print(cls, name: str, value: object = __DO_NOT_OUTPUT) -> None:
        """Output the name and value.

        Args:
            name: The name of the value or a message
            value: The value to output
        """
        if not cls.is_enabled: return

        cls.__data_nest_level = 0
        cls.__reflected_objects.clear()

        if value is cls.__DO_NOT_OUTPUT:
            print(cls.__get_datetime_string() + ' ' + cls.__get_indent_string() + name)
        else:
            value_strings = cls.__to_strings(value)
            first_line = True
            for value_string in value_strings:
                line = cls.__get_datetime_string() + ' ' + cls.__get_indent_string()
                if  first_line:
                    line += name + cls.varname_value_separator
                line += value_string
                print(line)
                first_line = False
