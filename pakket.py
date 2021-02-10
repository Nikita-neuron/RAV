
import ctypes
from ctypes import (
    c_int8, c_uint8,
    c_int16, c_uint16,
    c_int32, c_uint32,
    c_int64, c_uint64,
)
import struct
from typing import Union, Tuple

i8 = c_int8; u8 = c_uint8
i16 = c_int16; u16 = c_uint16
i32 = c_int32; u32 = c_uint32
i64 = c_int64; u64 = c_uint64
# _CData = i8.__base__.__base__
# _PyCStructType = ctypes.Structure.__class__

class DataMeta(type):
    def __new__(cls, name, bases, d: dict):
        return super().__new__(cls, name, bases, d)
    def __getitem__(self, item):
        return self._pakkit_annot(self, item)

class Data(metaclass=DataMeta):
    def _getformat(self) -> str:
        raise NotImplementedError()
    
    def _pakkit_frombytes(self, data_view: bytearray) -> Tuple['Data', int]:
        raise NotImplementedError()

class Array(Data):
    # def __init__(self, t: PakkitData, length: Union[int, Ellipsis] = ...):
    #     self.t = t
    #     self.length = length
    # def _pakkit_frombytes(self, data_view: bytearray) -> int:
    #     return 
    def _pakkit_annot(self, item):
        print('ANNOT', self, item)

class StructMeta(DataMeta):
    def __new__(cls, name, bases, d: dict):
        print(cls, name, bases, d)
        # _pakkit_fields_ = d.get('__pakkit_fields__', [])
        # __pakkit_format = ''
        # for annot_name, annot_type in d['__annotations__'].items():
        #     print(annot_name, annot_type)
        #     if issubclass(annot_type, Data):
        #         _pakkit_fields_.append((annot_name, annot_type))
        super().__new__(cls, name, bases, d)
    # def _frombytes

class Struct(metaclass=StructMeta):
    _pakkit_fields_ = 123
    # i: i8
    pass

'''
class MyStruct(Struct):
    i: i8
    arr: Array(8, )
'''

print(Array[int, ...])

class Loh:
    def __getitem__(self, x):
        return self
    def __getattribute__(self, name: str):
        return self

Loh().n.i.k.i.t.a[0].l.o.h[1][2][3][69][228]['duofdiuf']
