[en](./README.md)

# Python.sqlite3.row_factory.tuple.sqlite3row.namedtuple.dataclass.__getitem__

　SQLite3のselect結果をtuple,sqlite3.Row,namedtuple,dataclassで返す薄いラッパー。

<!--

# デモ

* [demo](https://ytyaru.github.io/Python.Python.sqlite3.row_factory.tuple.sqlite3row.namedtuple.dataclass.__getitem__.20221017181058/)

![img](https://github.com/ytyaru/Python.Python.sqlite3.row_factory.tuple.sqlite3row.namedtuple.dataclass.__getitem__.20221017181058/blob/master/doc/0.png?raw=true)

# 特徴

* セールスポイント

-->

# 開発環境

* <time datetime="2022-10-17T18:10:37+0900">2022-10-17</time>
* [Raspbierry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 4 Model B Rev 1.2
* [Raspberry Pi OS](https://ja.wikipedia.org/wiki/Raspbian) buster 10.0 2020-08-20 <small>[setup](http://ytyaru.hatenablog.com/entry/2020/10/06/111111)</small>
* bash 5.0.3(1)-release
* Python 3.10.5

<!-- * Python 2.7.16 -->

```sh
$ uname -a
Linux raspberrypi 5.10.103-v7l+ #1529 SMP Tue Mar 8 12:24:00 GMT 2022 armv7l GNU/Linux
```

# インストール

## anyenv

```sh
git clone https://github.com/anyenv/anyenv ~/.anyenv
echo 'export PATH="$HOME/.anyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(anyenv init -)"' >> ~/.bash_profile
anyenv install --init -y
```

## pyenv

```sh
anyenv install pyenv
exec $SHELL -l
```

## python

```sh
sudo apt install -y libsqlite3-dev libbz2-dev libncurses5-dev libgdbm-dev liblzma-dev libssl-dev tcl-dev tk-dev libreadline-dev
```

```sh
pyenv install -l
```
```sh
pyenv install 3.10.5
```


## このリポジトリ

```sh
git clone https://github.com/ytyaru/Python.Python.sqlite3.row_factory.tuple.sqlite3row.namedtuple.dataclass.__getitem__.20221017181058
cd Python.Python.sqlite3.row_factory.tuple.sqlite3row.namedtuple.dataclass.__getitem__.20221017181058/src
```

# 使い方

## 単体テスト

```sh
./test-ntlite.py
```

## import

```python
from ntlite import NtLite
```

## new

```python
db = NtLite() # :memory:
```
```python
db = NtLite('./db/my.sqlite3')
```
```python
db = NtLite('./db/my.sqlite3', RowTypes.dataclass)
```
```python
db = NtLite(path='./db/my.sqlite3', row_type=RowTypes.dataclass)
```

### RowTypes

RowTypes|column reference
--------|----------------
`RowTypes.tuple`|`row[0]`
`RowTypes.sqlite3row`([sqlite3.Row][])|`row[0]`, `row['col_name']`
`RowTypes.namedtuple`|`row[0]`, `row.col_name`, `row['col_name']`
`RowTypes.dataclass`|`row[0]`, `row.col_name`, `row['col_name']`

　RowTypesを指定することでDBの表から返された行の型をそれに指定できる。[row_factory][]で実装した。

#### RowTypes params

　以下の2つはパラメータを持っている。

```python
RowTypes.namedtuple(not_getitem=True)
```

```python
RowTypes.namedtuple(not_getitem=True, not_slot=True, not_frozen=True)
```

parameter|namedtuple|dataclass
---------|----------|---------
`not_getitem`=`True`|`['col_name']`で参照不可|`[0]`や`['col_name']`で参照不可
`not_slot`=`True`|-|新しいプロパティを登録できなくなる
`not_frozen`=`True`|-|ミュータブルになる（プロパティに値をセットできるようになる）

　デフォルトはすべて`False`。

　`NtLite`を生成するとき以下のように渡す。

```python
db = NtLite(row_type=RowTypes.namedtuple(not_getitem=True))
db = NtLite(row_type=RowTypes.dataclass(not_getitem=True, not_slot=True, not_frozen=True))
```

## SQL実行

method|call sqlite3 method
------|-------------------
`exec`|[execute][]
`execm`|[executemany][]
`execs`|[executescript][]
`get`|[execute][] + [fetchone][]
`gets`|[execute][] + [fetchall][]

[execute]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.execute
[executemany]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.executemany
[executescript]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Connection.executescript
[fetchone]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.fetchone
[fetchall]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.fetchall
[fetchmany]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.fetchmany

## 列参照

```python
row = db.get("select id, name num from users where id=5;")
row.id    #=> 5
row['id'] #=> 5
row[0]    #=> 5
```

[row_factory][]|reference
---------------|---------
RowTypes.tuple|`row[0]`
RowTypes.sqlite3row([sqlite3.Row][])|`row[0]`, `row['col_name']`
RowTypes.namedtuple|`row[0]`, `row.col_name`, `row['col_name']`
RowTypes.dataclass|`row[0]`, `row.col_name`, `row['col_name']`

[namedtuple ver]:https://github.com/ytyaru/Python.sqlite3.row_factory.namedtuple.20221015151253
[namedtuple + getitem ver]:https://github.com/ytyaru/Python.sqlite3.row_factory.namedtuple.__getitem__.20221016095117
[dataclass + getitem ver]:https://github.com/ytyaru/Python.sqlite3.row_factory.dataclass.20221016164153

[sqlite3]:https://docs.python.org/ja/3/library/sqlite3.html
[row_factory]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Connection.row_factory
[sqlite3.Row]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Row
[__getitem__]:https://docs.python.org/ja/3/reference/datamodel.html#object.__getitem__
[cursor.description]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.description
[namedtuple]:https://docs.python.org/ja/3/library/collections.html#collections.namedtuple
[dataclass]:https://docs.python.org/ja/3/library/dataclasses.html
[mypy]:https://github.com/python/mypy

## 例

```python
#!/usr/bin/env python3
# coding: utf8
import os
from ntlite import NtLite
path = 'my.db'
if os.path.isfile(path): os.remove(path)
db = NtLite(path)
db.exec("create table users(id integer, name text);")
db.execm("insert into users values(?,?);", [(0,'A'),(1,'B')])
assert 2 == db.get("select count(*) num from users;").num
rows = db.gets("select * from users;")
assert 0   == rows[0].id
assert 'A' == rows[0].name
assert 1   == rows[1].id
assert 'B' == rows[1].name

assert 0   == rows[0]['id']
assert 'A' == rows[0]['name']
assert 1   == rows[1]['id']
assert 'B' == rows[1]['name']

assert 0   == rows[0][0]
assert 'A' == rows[0][1]
assert 1   == rows[1][0]
assert 'B' == rows[1][1]
```

<!--

# 注意

* 注意点など

-->

# 著者

　ytyaru

* [![github](http://www.google.com/s2/favicons?domain=github.com)](https://github.com/ytyaru "github")
* [![hatena](http://www.google.com/s2/favicons?domain=www.hatena.ne.jp)](http://ytyaru.hatenablog.com/ytyaru "hatena")
* [![twitter](http://www.google.com/s2/favicons?domain=twitter.com)](https://twitter.com/ytyaru1 "twitter")
* [![mastodon](http://www.google.com/s2/favicons?domain=mstdn.jp)](https://mstdn.jp/web/accounts/233143 "mastdon")

# ライセンス

　このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

