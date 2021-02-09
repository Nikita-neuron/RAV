
import ctypes
from ctypes import (
    c_int8, c_uint8,
    c_int16, c_uint16,
    c_int32, c_uint32,
    c_int64, c_uint64,
)

i8 = c_int8; u8 = c_uint8
i16 = c_int16; u16 = c_uint16
i32 = c_int32; u32 = c_uint32
i64 = c_int64; u64 = c_uint64
_CData = i8.__base__.__base__
_PyCStructType = ctypes.Structure.__class__


class StructMeta(_PyCStructType):
    def __init__(self, name, bases, d):
        # print(self, name, bases, d)
        # _fields_ = []
        # for annot_name, annot_type in d['__annotations__'].items():
        #     print(annot_name, annot_type)
        #     if issubclass(annot_type, _CData):
        #         _fields_.append((annot_name, annot_type))
        d['_fields_'] = _fields_
        # print(_fields_)
        _fields_ = [('i', i8)]
        self._fields_ = _fields_
        super().__init__(name, bases, d)

class Struct(ctypes.Structure, metaclass=StructMeta):
    # i: i8
    pass

print(Struct().i)
