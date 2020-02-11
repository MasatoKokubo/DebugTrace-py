#################
DebugTrace-python
#################

**DebugTrace-python** は、Pythonのデバッグ時にトレースログを出力するライブラリで、 Python 3.5以降に対応しています。
メソッドの開始箇所に "``_ = debugtrace.enter()``" を埋め込む事で、開発中のプログラムの実行状況を出力する事ができます。

1. 特徴
=======

* ``debugtrace.enter()`` のコール元のメソッド名、ソースファイル名および行番号を自動的に出力。
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

以下は、DebugTrace-pythonを使用したPythonプログラムの例とそれを実行した際のログです。

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

    2020-02-11 20:53:08.082640 DebugTrace-python 1.0.0b10 -> sys.stderr
    2020-02-11 20:53:08.082744 
    2020-02-11 20:53:08.085611 Enter func1 (ReadmeExample.py:23)
    2020-02-11 20:53:08.085774 |   Enter func2 (ReadmeExample.py:15)
    2020-02-11 20:53:08.085896 |   |   Enter Contact.__init__ (ReadmeExample.py:8)
    2020-02-11 20:53:08.085958 |   |   Leave Contact.__init__ (ReadmeExample.py:8) time: 0:00:00.000008
    2020-02-11 20:53:08.086038 |   |   
    2020-02-11 20:53:08.086077 |   |   Enter Contact.__init__ (ReadmeExample.py:8)
    2020-02-11 20:53:08.086123 |   |   Leave Contact.__init__ (ReadmeExample.py:8) time: 0:00:00.000004
    2020-02-11 20:53:08.086474 |   |   contact = (list)[
    2020-02-11 20:53:08.086516 |   |     (__main__.Contact){
    2020-02-11 20:53:08.086533 |   |       birthday: 1991-02-03, firstName: (length:5)'Akane', id: 1, lastName: (length:5)'Apple'
    2020-02-11 20:53:08.086560 |   |     }, 
    2020-02-11 20:53:08.086591 |   |     (__main__.Contact){
    2020-02-11 20:53:08.086605 |   |       birthday: 1992-03-04, firstName: (length:6)'Yukari', id: 2, lastName: (length:5)'Apple'
    2020-02-11 20:53:08.086613 |   |     }
    2020-02-11 20:53:08.086638 |   |   ]
    2020-02-11 20:53:08.086680 |   Leave func2 (ReadmeExample.py:15) time: 0:00:00.000851
    2020-02-11 20:53:08.086724 Leave func1 (ReadmeExample.py:23) time: 0:00:00.001032

4. 関数
=========================

主に以下の関数があります。

.. list-table:: 関数一覧
    :widths: 10, 45, 45
    :header-rows: 1

    * - 名 前
      - 引数
      - 説 明
    * - ``enter``
      - **invoker** (object): 呼び出し元のselfまたはclsを渡します。 (省略可)
      - | 開始ログを出力します。
        | またコードブロックの終了時に終了ログを出力します。
        |
        | *使用例:*
        | ``_ = debugtrace.enter(self)``
        | ``_ = debugtrace.enter(cls)``
        | ``_ = debugtrace.enter()``
    * - ``print``
      - | **name** (str): 変数名など
        | **value** (object): 出力する値 (省力した場合はnameのみを出力)
        | **output_private** (bool): Trueならプライベートメンバーを出力する(default: False)
        | **output_method** (bool): Trueならメソッドを出力する (default: False)
      - | 変数名と値を出力します。
        |
        | *使用例:*
        | ``debugtrace.print('Hellow')``
        | ``debugtrace.print('foo', foo)``


5. **debugtrace.ini** ファイルで指定可能なオプション
====================================================

DebugTrace-python は、カレントディレクトリにある ``debugtrace.ini`` ファイルを初期化に読み込みます。
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
    * - ``enter_string``
      - 関数またはメソッドに入る際に出力する文字列
      - ``Enter``
    * - ``leave_string``
      - 関数またはメソッドから出る際に出力する文字列
      - ``Leave``
    * - ``limit_string``
      - 制限を超えた場合に出力する文字列
      - ``...``
    * - ``maximum_indents``
      - インデントの最大数
      - ``20``
    * - ``code_indent_string``
      - コードのインデント文字列
      - ｜␠␠␠
    * - ``data_indent_string``
      - データのインデント文字列
      - | ␠␠
        | (スペース2個)
    * - ``non_output_string``
      - 値を出力しない場合に代わりに出力する文字列
      - ``...``
    * - ``cyclic_reference_string``
      - 循環参照している場合に出力する文字列
      - ``*** Cyclic Reference ***``
    * - ``varname_value_separator``
      - 変数名と値のセパレータ文字列
      - ``␠=␠``
    * - ``key_value_separator``
      - | 辞書のキーと値のセパレータ
        | および属性名と属性値のセパレータ
      - ``:␠``
    * - ``log_datetime_format``
      - ``logger`` が ``StdOut`` または ``StdErr`` の場合のログの日時フォーマット
      - ``%Y-%m-%d %H:%M:%S.%f``
    * - ``enter_format``
      - | 関数またはメソッドに入る際に出力するログのフォーマット
        | ``{0}: 関数名またはメソッド名``
        | ``{1}: ファイル名``
        | ``{2}: 行番号``
      - ``{0} ({1}:{2})``
    * - ``leave_format``
      - | 関数またはメソッドを出る際に出力するログのフォーマット
        | ``{0}: 関数名またはメソッド名``
        | ``{1}: ファイル名``
        | ``{2}: 行番号``
        | ``{3}: 処理時間``
      - ``{0} ({1}:{2}) time: {3}``
    * - ``count_format``
      - ``list``, ``tuple``, ``dict`` 等の要素数の出力フィーマット
      - ``count:{}``
    * - ``minimum_output_count``
      - ``list``, ``tuple``, ``dict`` 等の要素数を出力する最小値
      - ``5``
    * - ``length_format``
      - 文字列, ``bytes`` の要素数の出力フォーマット
      - ``length:{}``
    * - ``minimum_output_length``
      - 文字列, ``bytes`` の要素数を出力する最小値
      - ``5``
    * - ``maximum_data_output_width``
      - データの出力幅の最大値
      - ``80``
    * - ``bytes_count_in_line``
      - ``bytes`` の内容の1行の出力数
      - ``16``
    * - ``collection_limit``
      - ``list``, ``tuple``, ``dict`` 等の要素を出力数の制限
      - ``256``
    * - ``string_limit``
      - 文字列値の出力文字数の制限
      - ``2048``
    * - ``bytes_limit``
      - ``bytes`` の内容の出力数の制限
      - ``512``
    * - ``reflection_nest_limit``
      - リフレクションのネスト数の制限
      - ``4``

6. ライセンス
=============

MIT ライセンス(MIT)

7. リリースノート
==================

``DebugTrace-python 1.0.0b10 - 2020-02-11``
------------------------------------------

* 改善とバグ修正

``DebugTrace-python 1.0.0b9 - 2020-02-09``
------------------------------------------

* 改善とバグ修正

``DebugTrace-python 1.0.0b8 - 2020-02-07``
------------------------------------------

* 改善とバグ修正

``DebugTrace-python 1.0.0b7 - 2020-02-05``
------------------------------------------

* 改善とバグ修正

``DebugTrace-python 1.0.0b6 - 2020-02-04``
------------------------------------------

* 改善とバグ修正

``DebugTrace-python 1.0.0b5 - 2020-02-03``
------------------------------------------

* 改善とバグ修正

``DebugTrace-python 1.0.0b4 - 2020-01-31``
------------------------------------------

* ``print_`` 関数名を ``print`` に変更

``DebugTrace-python 1.0.0b2 - 2020-01-13``
------------------------------------------

* 最初のリリース (beta版)

*(C) 2020 Masato Kokubo*
