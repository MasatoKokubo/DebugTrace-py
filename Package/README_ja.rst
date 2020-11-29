#############
DebugTrace-py
#############

**DebugTrace-py** は、Pythonのデバッグ時にトレースログを出力するライブラリで、 Python 3.7以降に対応しています。
メソッドの開始箇所に "``_ = debugtrace.enter()``" を埋め込む事で、開発中のプログラムの実行状況を出力する事ができます。

1. 特徴
=======

* ``debugtrace.enter()`` の呼び出し元のメソッド名、ソースファイル名および行番号を自動的に出力。
* またそのスコープ終了時に終了ログを出力。
* メソッドやオブジェクトのネストで、ログを自動的にインデント 。
* 値の出力で自動的に改行。
* ``__str__`` メソッドを実装していないクラスのオブジェクトでもリフレクションを使用して内容を出力。
* ``debugtrace.ini`` ファイルの設定で、出力内容のカスタマイズが可能。
* ``sys.stdout``, ``sys.stderr`` または ``logging`` パッケージを選択して出力可能

2. インストール
===============

``pip install debugtrace``

3. 使用方法
===========

デバッグ対象および関連する関数またはメソッドに対して以下を行います。

* 関数またはメソッドの先頭に "``_ = debugtrace.enter()``" を挿入する。
* 必要に応じて変数をログに出力する "``debugtrace.print('foo', foo)``" を挿入する。

以下は、DebugTrace-pyを使用したPythonプログラムの例とそれを実行した際のログです。

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

ログの出力内容:
::

    2020-11-29 14:02:36.423205 DebugTrace-py 1.0.2
    2020-11-29 14:02:36.423264   config file path: <No config file>
    2020-11-29 14:02:36.423343 　logger: sys.stderr
    2020-11-29 14:02:36.423358 
    2020-11-29 14:02:36.427672 Enter func1 (ReadmeExample.py:22)
    2020-11-29 14:02:36.427836 | Enter func2 (ReadmeExample.py:14)
    2020-11-29 14:02:36.427922 | | Enter Contact.__init__ (ReadmeExample.py:7)
    2020-11-29 14:02:36.427959 | | Leave Contact.__init__ (ReadmeExample.py:7) duration: 0:00:00.000006
    2020-11-29 14:02:36.428039 | | 
    2020-11-29 14:02:36.428061 | | Enter Contact.__init__ (ReadmeExample.py:7)
    2020-11-29 14:02:36.428086 | | Leave Contact.__init__ (ReadmeExample.py:7) duration: 0:00:00.000004
    2020-11-29 14:02:36.428705 | | 
    2020-11-29 14:02:36.428732 | | contacts = (list)[
    2020-11-29 14:02:36.428743 | |   (__main__.Contact){
    2020-11-29 14:02:36.428751 | |     birthday: 1991-02-03, firstName: (length:5)'Akane', id: 1,
    2020-11-29 14:02:36.428758 | |     lastName: (length:5)'Apple'
    2020-11-29 14:02:36.428765 | |   },
    2020-11-29 14:02:36.428772 | |   (__main__.Contact){
    2020-11-29 14:02:36.428779 | |     birthday: 1992-03-04, firstName: (length:6)'Yukari', id: 2,
    2020-11-29 14:02:36.428787 | |     lastName: (length:5)'Apple'
    2020-11-29 14:02:36.428794 | |   }
    2020-11-29 14:02:36.428800 | | ] (ReadmeExample.py:19)
    2020-11-29 14:02:36.428812 | | 
    2020-11-29 14:02:36.428829 | Leave func2 (ReadmeExample.py:14) duration: 0:00:00.000954
    2020-11-29 14:02:36.428848 Leave func1 (ReadmeExample.py:22) duration: 0:00:00.001123

4. 関数
=========================

主に以下の関数があります。

.. list-table:: 関数一覧
    :widths: 10, 90
    :header-rows: 1

    * - 名 前
      - 説 明
    * - ``enter``
      - | 開始ログを出力します。
        | またコードブロックの終了時に終了ログを出力します。
        |
        | *引数:*
        | **invoker** (``object, optional``): 呼び出し元の ``self`` または ``cls`` を渡します。
        |
        | *使用例:*
        | ``_ = debugtrace.enter(self)``
        | ``_ = debugtrace.enter(cls)``
        | ``_ = debugtrace.enter()``
    * - ``print``
      - | 変数名と値を出力します。
        |
        | *引数:*
        | **name** (``str``): 変数名など
        | **value** (``object``): 出力する値 (省力した場合はnameのみを出力)
        |
        | 以下はキーワード引数で省略可能
        |
        | **force_reflection** (``bool``): Trueならプライベートメンバーを出力する (デフォルト: ``False``)
        | **output_private** (``bool``): Trueならプライベートメンバーを出力する (デフォルト: ``False``)
        | **output_method** (``bool``): Trueならメソッドを出力する (デフォルト: ``False``)
        | **collection_limit** (``int``): ``list``, ``tuple``, ``dict`` 等の要素の出力数の制限値 (デフォルト: ``None``)
        | **bytes_limit** (``int``): ``bytes`` および ``bytearray`` の要素の出力数の制限値 (デフォルト: ``None``)
        | **string_limit** (``int``): 文字列値の出力文字数の制限値 (デフォルト: ``None``)
        | **reflection_nest_limit** (int): リフレクションのネスト数の制限値 (デフォルト: ``None``)
        |
        | *使用例:*
        | ``debugtrace.print('Hellow')``
        | ``debugtrace.print('foo', foo)``
        | ``debugtrace.print('foo', foo, force_reflection=True)``
        | ``debugtrace.print('foos', foos, collection_limit=1024)``


5. **debugtrace.ini** ファイル
====================================================

DebugTrace-py は、カレントディレクトリにある ``debugtrace.ini`` ファイルを初期化に読み込みます。
セクションは、``[debugtrace]`` です。

``debugtrace.ini`` ファイルで以下のオプションを指定できます。

.. list-table:: ``debugtrace.ini``
    :widths: 30, 50, 20
    :header-rows: 1

    * - オプション名
      - 説 明
      - デフォルト値
    * - ``logger``
      - | debugtraceが使用するロガー
        | ``StdOut: sys.stdoutへ出力``
        | ``StdErr: sys.stderrへ出力``
        | ``Logger: loggingパッケージを使用して出力``
      - ``StdErr``
    * - ``logging_config_file``
      - loggingパッケージに指定する設定ファイル名
      - ``logging.conf``
    * - ``logging_logger_name``
      - loggingパッケージを使用する場合のロガー名
      - ``debugtrace``
    * - ``logging_level``
      - loggingパッケージを使用する場合のログレベル
      - ``DEBUG``
    * - ``is_enabled``
      - | ``False: ログ出力が無効``
        | ``True: ログ出力が有効``
      - ``True``
    * - ``enter_format``
      - | 関数またはメソッドに入る際に出力するログのフォーマット文字列
        | ``{0}: 関数名またはメソッド名``
        | ``{1}: ファイル名``
        | ``{2}: 行番号``
      - ``Enter {0} ({1}:{2})``
    * - ``leave_format``
      - | 関数またはメソッドを出る際に出力するログのフォーマット文字列
        | ``{0}: 関数名またはメソッド名``
        | ``{1}: ファイル名``
        | ``{2}: 行番号``
        | ``{3}: 処理時間``
      - ``Leave {0} ({1}:{2}) time: {3}``
    * - ``maximum_indents``
      - インデントの最大数
      - ``20``
    * - ``indent_string``
      - コードのインデント文字列
      - ``｜\s``
    * - ``data_indent_string``
      - データのインデント文字列
      - ``\s\s``
    * - ``limit_string``
      - 制限を超えた場合に出力する文字列
      - ``...``
    * - ``non_output_string``
      - | 値を出力しない場合に代わりに出力する文字列
        | (現在未使用)
      - ``...``
    * - ``cyclic_reference_string``
      - 循環参照している場合に出力する文字列
      - ``*** Cyclic Reference ***``
    * - ``varname_value_separator``
      - 変数名と値のセパレータ文字列
      - ``\s=\s``
    * - ``key_value_separator``
      - 辞書のキーと値および属性名と属性値のセパレータ文字列
      - ``:\s``
    * - ``print_suffix_format``
      - `print` メソッドで付加される文字列のフォーマット
      - ``\s({1}:{2})``
    * - ``count_format``
      - ``list``, ``tuple``, ``dict`` 等の要素数のフォーマット
      - ``count:{}``
    * - ``minimum_output_count``
      - ``list``, ``tuple``, ``dict`` 等の要素数を出力する最小値
      - ``5``
    * - ``length_format``
      - 文字列, ``bytes`` の要素数のフォーマット
      - ``length:{}``
    * - ``minimum_output_length``
      - 文字列, ``bytes`` の要素数を出力する最小値
      - ``5``
    * - ``log_datetime_format``
      - | ``logger`` が ``StdOut`` または ``StdErr`` の場合のログの日時のフォーマット
        | (現在設定不可)
      - ``%Y-%m-%d %H:%M:%S.%f``
    * - ``maximum_data_output_width``
      - データの出力幅の最大値
      - ``70``
    * - ``bytes_count_in_line``
      - ``bytes`` の内容の1行の出力数
      - ``16``
    * - ``collection_limit``
      - ``list``, ``tuple``, ``dict`` 等の要素の出力数の制限値
      - ``512``
    * - ``string_limit``
      - 文字列値の出力文字数の制限値
      - ``8192``
    * - ``bytes_limit``
      - ``bytes`` および ``bytearray`` の要素の出力数の制限値
      - ``8192``
    * - ``reflection_nest_limit``
      - リフレクションのネスト数の制限値
      - ``4``

``\s`` *はスペースに変換します。*

6. ライセンス
=============

MIT ライセンス(MIT)

7. リリースノート
==================

``DebugTrace-py 1.0.2 - 2020-11-29``
------------------------------------

* 開始時のメッセージの変更 (``'DebugTrace-py ...'`` <- ``'DebugTrace-python ...'``)

``DebugTrace-py 1.0.1 - 2020-07-19``
------------------------------------

* データ出力の改行処理を改善

``DebugTrace-py 1.0.0 - 2020-05-26``
------------------------------------

* 最初のリリース

*(C) 2020 Masato Kokubo*
