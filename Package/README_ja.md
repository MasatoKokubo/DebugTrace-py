# DebugTrace-py

**DebugTrace-py** は、Pythonのデバッグ時にトレースログを出力するライブラリで、 Python 3.7以降に対応しています。
メソッドの開始箇所に "`_ = debugtrace.enter()`" を埋め込む事で、開発中のプログラムの実行状況を出力する事ができます。

## 1. 特徴

* `debugtrace.enter()` の呼び出し元のメソッド名、ソースファイル名および行番号を自動的に出力。
* またそのスコープ終了時に終了ログを出力。
* メソッドやオブジェクトのネストで、ログを自動的にインデント 。
* 値の出力で自動的に改行。
* `__str__` メソッドを実装していないクラスのオブジェクトでもリフレクションを使用して内容を出力。
* `debugtrace.ini`ファイルの設定で、出力内容のカスタマイズが可能。
* `sys.stdout`, `sys.stderr`または`logging`パッケージを選択して出力可能

## 2. インストール

`pip install debugtrace`

## 3. 使用方法

デバッグ対象および関連する関数またはメソッドに対して以下を行います。

* 関数またはメソッドの先頭に `_ = debugtrace.enter()` を挿入する。
* 必要に応じて変数をログに出力する `debugtrace.print('foo', foo)` を挿入する。

以下は、DebugTrace-pyを使用したPythonプログラムの例とそれを実行した際のログです。

```python:readme_example.py
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
```

ログの出力内容:
```log
2023-02-26 21:05:06.623919+0900 DebugTrace-py 1.3.0 on Python 3.11.0
2023-02-26 21:05:06.623973+0900   config file path: <No config file>
2023-02-26 21:05:06.623990+0900   logger: sys.stderr
2023-02-26 21:05:06.624044+0900 
2023-02-26 21:05:06.624091+0900 ______________________________ MainThread #140621580739648 ______________________________
2023-02-26 21:05:06.624106+0900 
2023-02-26 21:05:06.625608+0900 Enter func1 (readme_example.py:22) <- (readme_example.py:26)
2023-02-26 21:05:06.625701+0900 | Hello, World! (readme_example.py:23)
2023-02-26 21:05:06.625806+0900 | Enter func2 (readme_example.py:14) <- (readme_example.py:24)
2023-02-26 21:05:06.625902+0900 | | Enter Contact.__init__ (readme_example.py:7) <- (readme_example.py:16)
2023-02-26 21:05:06.625964+0900 | | Leave Contact.__init__ (readme_example.py:7) duration: 0:00:00.000008
2023-02-26 21:05:06.626055+0900 | | 
2023-02-26 21:05:06.626091+0900 | | Enter Contact.__init__ (readme_example.py:7) <- (readme_example.py:17)
2023-02-26 21:05:06.626123+0900 | | Leave Contact.__init__ (readme_example.py:7) duration: 0:00:00.000005
2023-02-26 21:05:06.627114+0900 | | 
2023-02-26 21:05:06.627155+0900 | | contacts = [
2023-02-26 21:05:06.627190+0900 | |   (__main__.Contact){
2023-02-26 21:05:06.627218+0900 | |     birthday: 1991-02-03, firstName: 'Akane', id: 1, lastName: 'Apple'
2023-02-26 21:05:06.627235+0900 | |   },
2023-02-26 21:05:06.627246+0900 | |   (__main__.Contact){
2023-02-26 21:05:06.627257+0900 | |     birthday: 1992-03-04, firstName: 'Yukari', id: 2, lastName: 'Apple'
2023-02-26 21:05:06.627279+0900 | |   }
2023-02-26 21:05:06.627314+0900 | | ] (readme_example.py:19)
2023-02-26 21:05:06.627348+0900 | | 
2023-02-26 21:05:06.627390+0900 | Leave func2 (readme_example.py:14) duration: 0:00:00.001537
2023-02-26 21:05:06.627430+0900 Leave func1 (readme_example.py:22) duration: 0:00:00.001769
```

## 4. 関数

主に以下の関数があります。

<table>
    <caption>関数一覧<caption>
    <tr><th>名 前</th><th>説 明</th></tr>
    <tr>
        <td><code>enter</code></td>
        <td>
            開始ログを出力します。<br>
            またコードブロックの終了時に終了ログを出力します。<br>
            <br>
            <i>引数:</i><br>
            <code><b>invoker</b> (object, optional)</code>: 呼び出し元の<code>self</code>または<code>cls</code>を渡します。<br>
            <br>
            <i>使用例:</i><br>
            <code>
                _ = debugtrace.enter(self)<br>
                _ = debugtrace.enter(cls)<br>
                _ = debugtrace.enter()
            </code>
        </td>
    </tr>
    <tr>
        <td><code>print</code></td>
        <td>
            変数名と値を出力します。<br>
            <br>
            <i>引数:</i><br>
            <code><b>name</b> (str)</code>: 変数名など<br>
            <code><b>value</b> (object, optional)</code>: 出力する値(省力した場合はnameのみを出力)<br>
            <br>
            以下はキーワード引数<br>
            <br>
            <code><b>force_reflection</b> (bool, optional)</code>: <code>True</code>の場合、プライベートメンバーを出力する(デフォルト: <code>False</code>)<br>
            <code><b>output_private</b> (bool, optional)</code>: <code>True</code>の場合、プライベートメンバーを出力する(デフォルト: <code>False</code>)<br>
            <code><b>output_method</b> (bool, optional)</code>: <code>True</code>の場合、メソッドを出力する(デフォルト: <code>False</code>)<br>
            <code><b>collection_limit</b> (int, optional)</code>: <code>list</code>, <code>tuple</code>, <code>dict</code>等の要素の出力数の制限値(デフォルト: <code>None</code>)<br>
            <code><b>bytes_limit</b> (int, optional)</code>: <code>bytes</code>および<code>bytearray</code>の要素の出力数の制限値(デフォルト: <code>None</code>)<br>
            <code><b>string_limit</b> (int, optional)</code>: 文字列値の出力文字数の制限値(デフォルト: <code>None</code>)<br>
            <code><b>reflection_nest_limit</b> (int, optional)</code>: リフレクションのネスト数の制限値(デフォルト: <code>None</code>)<br>
            <br>
            <i>使用例:</i><br>
            <code>
                debugtrace.print('Hellow')<br>
                debugtrace.print('foo', foo)<br>
                debugtrace.print('foo', foo, force_reflection=True)<br>
                debugtrace.print('foos', foos, collection_limit=1024)
            </code>
        </td>
    </tr>
</table>

## 5. **debugtrace.ini** ファイル

DebugTrace-py は、カレントディレクトリにある`debugtrace.ini`ファイルを初期化に読み込みます。
セクションは、`[debugtrace]`です。

`debugtrace.ini`ファイルで以下のオプションを指定できます。

<table>
    <caption>debugtrace.ini<caption>
    <tr><th>オプション名</th><th>説 明</th><th>デフォルト値</th></tr>
    <tr>
        <td><code>logger</code></td>
        <td>
            debugtraceが使用するロガー<br>
            指定可能な値:<br>
            <code>stdout</code> - <code>sys.stdout</code>へ出力<br>
            <code>stderr</code> - <code>sys.stderr</code>へ出力<br>
            <code>logger</code> - <code>logging</code>パッケージを使用して出力<br>
            <code>file:</code><ログファイルのパス> - ファイルに直接出力
        </td>
        <td><code>stderr</code></td>
    </tr>
    <tr>
        <td><code>logging_config_file</code></td>
        <td>loggingパッケージに指定する設定ファイル名</td>
        <td><code>logging.conf</code></td>
    </tr>
    <tr>
        <td><code>logging_logger_name</code></td>
        <td>loggingパッケージを使用する場合のロガー名</td>
        <td><code>debugtrace</code></td>
    </tr>
    <tr>
        <td><code>is_enabled</code></td>
        <td>
            指定可能な値:<br>
           <code>False</code>: ログ出力が無効<br>
           <code>True</code>: ログ出力が有効
        </td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td><code>enter_format</code></td>
        <td>
            関数またはメソッドに入る際に出力するログのフォーマット文字列<br>
            <code>{0}</code>: 関数名またはメソッド名<br>
            <code>{1}</code>: ファイル名<br>
            <code>{2}</code>: 行番号<br>
            <code>{3}</code>: 呼び出し元のファイル名<br>
            <code>{4}</code>: 呼び出し元の行番号
        </td>
        <td><code>Enter {0} ({1}:{2}) <- ({3}:{4})</code></td>
    </tr>
    <tr>
        <td><code>leave_format</code></td>
        <td>
            関数またはメソッドを出る際に出力するログのフォーマット文字列<br>
            <code>{0}</code>: 関数名またはメソッド名<br>
            <code>{1}</code>: ファイル名<br>
            <code>{2}</code>: 行番号<br>
            <code>{3}</code>: 関数またはメソッドに入ってからの時間
        </td>
        <td><code>Leave {0} ({1}:{2}) duration: {3}</code></td>
    </tr>
    <tr>
        <td><code>thread_boundary_format</code></td>
        <td>
            スレッド境界のログ出力の文字列フォーマット<br>
            <code>{0}</code>: スレッド名<br>
            <code>{1}</code>: スレッドID
        </td>
        <td>
            <code>______________________________ {0} #{1} ______________________________</code>
        </td>
    </tr>
    <tr>
        <td><code>maximum_indents</code></td>
        <td>インデントの最大数</td>
        <td>32</td>
    </tr>
    <tr>
        <td><code>indent_string</code></td>
        <td>コードのインデント文字列</td>
        <td><code>\s</code></td>
    </tr>
    <tr>
        <td><code>data_indent_string</code></td>
        <td>データのインデント文字列</td>
        <td><code>\s\s<code></td>
    </tr>
    <tr>
        <td><code>limit_string<code></td>list
        <td>制限を超えた場合に出力する文字列</td>
        <td><code>...</code></td>
    </tr>
    <tr>
        <td><code>non_output_string</code><br>(現在未使用)</td>
        <td>値を出力しない場合に代わりに出力する文字列</td>
        <td><code>...</code></td>
    </tr>
    <tr>
        <td><code>cyclic_reference_string</code></td>
        <td>循環参照している場合に出力する文字列</td>
        <td><code>*** Cyclic Reference ***</code></td>
    </tr>
    <tr>
        <td><code>varname_value_separator</code></td>
        <td>変数名と値のセパレータ文字列</td>
        <td><code>\s=\s</code></td>
    </tr>
    <tr>
        <td><code>key_value_separator</code></td>
        <td>辞書のキーと値および属性名と属性値のセパレータ文字列</td>
        <td><code>:\s</code></td>
    </tr>
    <tr>
        <td><code>print_suffix_format<c/ode></td>
        <td><code>print</code>メソッドで付加される文字列のフォーマット</td>
        <td><code>\s({1}:{2})</code></td>
    </tr>
    <tr>
        <td><code>count_format</code></td>
        <td><code>list</code>, <code>tuple</code>, <code>dict</code>等の要素数のフォーマット</td>
        <td><code>count:{}</code></td>
    </tr>
    <tr>
        <td><code>minimum_output_count</code></td>
        <td><code>list</code>, <code>tuple</code>, <code>dict</code>等の要素数を出力する最小値</td>
        <td>16</td>
    </tr>
    <tr>
        <td><code>length_format</code></td>
        <td>文字列, <code>bytes</code>の要素数のフォーマット</td>
        <td><code>length:{}</code></td>
    </tr>
    <tr>
        <td><code>minimum_output_length</code></td>
        <td>文字列, <code>bytes</code>の要素数を出力する最小値</td>
        <td>16</td>
    </tr>
    <tr>
        <td><code>log_datetime_format</code></td>
        <td>
           <code>logger</code>が<code>StdOut</code>または<code>StdErr</code>の場合のログの日時のフォーマット
        </td>
        <td><code>%Y-%m-%d %H:%M:%S.%f%z</code></td>
    </tr>
    <tr>
        <td><code>maximum_data_output_width</code></td>
        <td>データの出力幅の最大値</td>
        <td>70</td>
    </tr>
    <tr>
        <td><code>bytes_count_in_line</code></td>
        <td><code>bytes</code>の内容の1行の出力数</td>
        <td>16</td>
    </tr>
    <tr>
        <td><code>collection_limit</code></td>
        <td><code>list</code>, <code>tuple</code>, <code>dict</code>等の要素の出力数の制限値</td>
        <td>128</td>
    </tr>
    <tr>
        <td><code>string_limit</code></td>
        <td>文字列値の出力文字数の制限値</td>
        <td>256</td>
    </tr>
    <tr>
        <td><code>bytes_limit</code></td>
        <td><code>bytes</code>および<code>bytearray</code>の要素の出力数の制限値</td>
        <td>256</td>
    </tr>
    <tr>
        <td><code>reflection_nest_limit</code></td>
        <td>リフレクションのネスト数の制限値</td>
        <td>4</td>
    </tr>
</table>

`\s` *はスペースに変換します。*

## 1. ライセンス

[MIT License (MIT)](LICENSE)

*&copy; 2020 Masato Kokubo*

## 7. リリースノート

### DebugTrace-py 1.3.0 - 2023/3/4

* `enter` メソッドのログ出力に、呼び出し元のソースファイル名と行番号を追加しました。 
* `debugtrace.ini`で`logging_level`の設定を廃止し、固定(`DEBUG`)にしました。
* `debugtrace.ini`の設定項目に`log_datetime_format`を追加しました。

### DebugTrace-py 1.2.0 - 2022/8/15

* 開始時のログに実行時のPythonのバージョンを追加しました。
* スレッドの切り替わりが分かるログを出力するようにしました。
* 以下のプロパティのデフォルト値を変更しました。

|プロパティ名|新デフォルト値|旧デフォルト値|
|:---------|:----------:|:----------:|
|minimum_output_count | 16|   5|
|minimum_output_length| 16|   5|
|collection_limit     |128| 512|
|string_limit         |256|8192|
|bytes_limit          |256|8192|

### DebugTrace-py 1.1.0 - 2021/11/28

* `__str__` または `__repr__` を実装しているクラスのオブジェクトを出力するとエラーになる不具合を修正しました。
* `tuple`, `set`, `dict` のデータ型を出力しないようにしました。  
    `(1, 2, 3)` &larr; `(tuple)(1, 2, 3)`  
    `(1,)` &larr; `(tuple)(1)`  
    `()` &larr; `(tuple)()`  
    `{1, 2, 3}` &larr; `(set){1, 2, 3}`  
    `{}` &larr; `(set){}`  
    `{1: 'A', 2: 'B', 3; 'C'}` &larr; `(dict){1: 'A', 2: 'B', 3; 'C'}`  
    `{:}` &larr; `(dict){}`  

### DebugTrace-py 1.0.3 - 2021/8/12

* データ出力の改行処理を改善

### DebugTrace-py 1.0.2 - 2020/11/29

* 開始時のメッセージの変更 (`'DebugTrace-py ...'` <- `'DebugTrace-python ...'`)

### DebugTrace-py 1.0.1 - 2020/7/19

* データ出力の改行処理を改善

### DebugTrace-py 1.0.0 - 2020/5/26

* 最初のリリース

*&copy; 2020 Masato Kokubo*
