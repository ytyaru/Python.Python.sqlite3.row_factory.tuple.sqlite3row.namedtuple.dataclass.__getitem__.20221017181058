import sqlite3
from collections import namedtuple
import dataclasses
import inspect
#from dataclasses import make_dataclass
RowTypes = namedtuple('RowTypes', 'tuple row namedtuple dataclass', defaults=(0,1,2,3))()
class RowType: pass
RowType.row_factory = None
class TupleRowType(RowType): pass
class Sqlite3RowType(RowType): pass
Sqlite3RowType.row_factory = sqlite3.Row
class NamedTupleRowType(RowType):
    def __init__(self, not_getitem=False): self._not_getitem = not_getitem
    def row_factory(self, cursor, row):
        row_type = self.new_row_type(cursor)
        if not self._not_getitem: row_type = self.set_getitem(row_type)
        return row_type(*row)
    def new_row_type(self, cursor): return namedtuple('Row', list(map(lambda d: d[0], cursor.description)))
    def set_getitem(self, row_type):
        def getitem(self, key):
            if isinstance(key, str): return getattr(self, key)
            else: return super(type(self), self).__getitem__(key)
        row_type.__getitem__ = getitem
        return row_type
class DataClassRowType(RowType):
    def __init__(self, not_getitem=False, not_slot=False, not_frozen=False):
        self._not_getitem = not_getitem
        self._not_slot = not_slot
        self._not_frozen = not_frozen
    def row_factory(self, cursor, row):
        row_type = self.new_row_type(cursor)
        if not self._not_getitem: row_type = self.set_getitem(row_type)
        return row_type(*row)
    def new_row_type(self, cursor):
        return dataclasses.make_dataclass('Row', list(tuple(map(lambda d: d[0], cursor.description))))
    def set_getitem(self, row_type):
        def getitem(self, key):
            if isinstance(key, str): return getattr(self, key)
            elif isinstance(key, int): return getattr(self, list(self.__annotations__.keys())[key])
            else: raise TypeError('The key should be int or str type.')
        row_type.__getitem__ = getitem
        return row_type
# NtLiteのコンストラクタ引数row_typeにセットする値はこのRowTypesが持ついずれかのプロパティを渡す
RowTypes = namedtuple('RowTypes', 'tuple sqlite3row namedtuple dataclass', defaults=(TupleRowType, Sqlite3RowType, NamedTupleRowType, DataClassRowType))()
"""
print(issubclass(RowType, RowType))
print(issubclass(TupleRowType, RowType))
print(issubclass(Sqlite3RowType, RowType))
print(issubclass(NamedTupleRowType, RowType))
print(issubclass(DataClassRowType, RowType))
print(issubclass(type(RowType()), RowType))
print(issubclass(type(TupleRowType()), RowType))
print(issubclass(type(Sqlite3RowType()), RowType))
print(issubclass(type(NamedTupleRowType()), RowType))
print(issubclass(type(DataClassRowType()), RowType))
"""
class NtLite:
    def __init__(self, path=':memory:', row_type=None):
        self._path = path
        self._row_type = row_type
        #self._row_type = row_type if issubclass(type(row_type), RowType) else NamedTupleRowType()
        self.RowType = row_type
        self._con = sqlite3.connect(path)
        #self._con.row_factory = self._dataclass_factory # sqlite3.Row, self._namedtuple_factory
        self._set_row_factory()
        self._cur = self._con.cursor()
    def __del__(self): self._con.close()
    def table_names(self): return [row.name for row in self.gets("select name from sqlite_master where type='table';")]
    def column_names(self, table_name): return [row.name for row in self.table_info(table_name)]
    def table_info(self, table_name): return self.gets(f"PRAGMA table_info('{table_name}');")
    def exec(self, sql, params=()): return self.con.execute(sql, params)
    def execm(self, sql, params=()): return self.con.executemany(sql, params)
    def execs(self, sql): return self.con.executescript(sql)
    def get(self, sql, params=()): return self.exec(sql, params).fetchone()
    def gets(self, sql, params=()): return self.exec(sql, params).fetchall()
    def commit(self): return self.con.commit()
    def rollback(self): return self.con.rollback()
    @property
    def con(self): return self._con
    @property
    def cur(self): return self._cur
    @property
    def path(self): return self._path
    @property
    def RowType(self): return self._row_type
    @RowType.setter
    def RowType(self, v):
        if inspect.isclass(v):
            if issubclass(v, RowType):
                self._row_type = v() # 型が渡されたらデフォルトコンストラクタで生成したインスタンスをセットする
                return
        self._row_type = v if issubclass(type(v), RowType) else NamedTupleRowType()
        #type(v)
        #self._row_type = v() if isinstance(v, type) and issubclass(v, RowType) else v if issubclass(type(v), RowType) else NamedTupleRowType()

        #self._row_type = v if issubclass(type(v), RowType) else NamedTupleRowType()
        #print('setter:', issubclass(type(v), RowType), v, self._row_type)
    def _set_row_factory(self):
        self._con.row_factory = self._row_type.row_factory if issubclass(type(self._row_type), RowType) else NamedTupleRowType().row_factory
        print(self._con.row_factory, self._row_type)
    """
    def _namedtuple_factory(self, cursor, row): return self._make_row_type(list(map(lambda d: d[0], cursor.description)))(*row)
    def _make_row_type(self, col_names): return self._set_getitem(namedtuple('Row', col_names))
    def _set_getitem(self, typ): #https://stackoverflow.com/questions/45326573/slicing-a-namedtuple
        def getitem(self, key):
            if isinstance(key, str): return getattr(self, key)
            else: return super(type(self), self).__getitem__(key)
        typ.__getitem__ = getitem
        return typ
    def _dataclass_factory(self, cursor, row):
        #return dataclasses.make_dataclass('Row', list(tuple(map(lambda d: d[0], cursor.description))))(*row)
        # AttributeError: 'super' object has no attribute '__getitem__'
        #return self._set_getitem(dataclasses.make_dataclass('Row', list(tuple(map(lambda d: d[0], cursor.description)))))(*row)
        return self._make_getitem(dataclasses.make_dataclass('Row', list(tuple(map(lambda d: d[0], cursor.description)))))(*row)
    def _make_getitem(self, typ): #https://stackoverflow.com/questions/45326573/slicing-a-namedtuple
        def getitem(self, key):
            if isinstance(key, str): return getattr(self, key)
            elif isinstance(key, int): return getattr(self, list(self.__annotations__.keys())[key])
            #elif isinstance(key, int): return getattr(self, self.__annotations__.keys()[key])
            else: raise TypeError('The key should be int or str type.')
        typ.__getitem__ = getitem
        return typ
    """

