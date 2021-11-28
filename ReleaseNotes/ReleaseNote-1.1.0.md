* Fixed a bug that an error occurs when outputting an object of a class that implements ``__str__`` or ``__repr__``. 
* Do not output ``tuple``, ``set``, ``dict`` data types.
    ``(1, 2, 3)`` ← ``(tuple)(1, 2, 3)``  
    ``(1,)`` ← ``(tuple)(1)``  
    ``()`` ← ``(tuple)()``  
    ``{1, 2, 3}`` ← ``(set){1, 2, 3}``  
    ``{}`` ← ``(set){}``  
    ``{1: 'A', 2: 'B', 3; 'C'}`` ← ``(dict){1: 'A', 2: 'B', 3; 'C'}``  
    ``{:}`` ← ``(dict){}``

----
*Japanese*

* ``__str__`` または ``__repr__`` を実装しているクラスのオブジェクトを出力するとエラーになる不具合を修正しました。
* ``tuple``, ``set``, ``dict`` のデータ型を出力しないようにしました。
    ``(1, 2, 3)`` ← ``(tuple)(1, 2, 3)``  
    ``(1,)`` ← ``(tuple)(1)``  
    ``()`` ← ``(tuple)()``  
    ``{1, 2, 3}`` ← ``(set){1, 2, 3}``  
    ``{}`` ← ``(set){}``  
    ``{1: 'A', 2: 'B', 3; 'C'}`` ← ``(dict){1: 'A', 2: 'B', 3; 'C'}``  
    ``{:}`` ← ``(dict){}``
