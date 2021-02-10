
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

class DataTypeMeta(type):
    def __new__(cls, name, bases, d: dict):
        print('METANEW')
        return super().__new__(cls, name, bases, d)
    def __getitem__(self, args):
        print('GETITEM', self, args)
        if type(args) == tuple:
            return self(*args)
        return self(args)

class DataType(type, metaclass=DataTypeMeta):
    def __new__(cls, *args): # SHOULD BE IMPLEMENTED IN SUBCLASSES 
        print('DTYPENEW', cls, args, '|', cls.__name__, cls.__bases__, cls.__dict__)
        #                              #TODO
        #                     (может можно сделать имя получше)
        return super().__new__(cls, cls.__name__, (), dict(cls.__dict__))
    def __init__(self, *args):
        print('DATATYPE INIT')
        # super().__init__(self, *args)

class Array(DataType):
    # def __init__(self, t: PakkitData, length: Union[int, Ellipsis] = ...):
    #     self.t = t
    #     self.length = length
    # def __pakkit_init__(self, dtype: Data, size=...):
    #     self.dtype = dtype
    #     self.size = size
    def __init__(self, *args):
        print('ARRAYTYPE INIT', args)

class ArrayInstance(metaclass=Array):
    def __init__(self, lst):
        print('ACTUAL INIT', lst)

# class StructMeta(DataMeta):
#     def __new__(cls, name, bases, d: dict):
#         print(cls, name, bases, d)
#         # _pakkit_fields_ = d.get('__pakkit_fields__', [])
#         # __pakkit_format = ''
#         # for annot_name, annot_type in d['__annotations__'].items():
#         #     print(annot_name, annot_type)
#         #     if issubclass(annot_type, Data):
#         #         _pakkit_fields_.append((annot_name, annot_type))
#         super().__new__(cls, name, bases, d)
#     # def _frombytes

# class Struct(metaclass=StructMeta):
#     _pakkit_fields_ = 123
#     # i: i8
#     pass

'''
class MyStruct(Struct):
    i: i8
    arr: Array[1,]
'''

o = ArrayInstance([1, 2, 3])
print('DONE', type(o))

