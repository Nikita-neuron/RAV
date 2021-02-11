
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
# _CData = i8.__base__.__base__
# _PyCStructType = ctypes.Structure.__class__


class Data(metaclass=):

class DataTypeMeta(type):
    def __getitem__(self, args):
        if type(args) == tuple:
            return self(*args)
        return self(args)

class DataType(type, metaclass=DataTypeMeta):
    # *args и **kwargs - аргументы для подклассов, они тут как заглушка
    def __new__(DataType, *args, **kwargs):
        print('DATATYPE NEW', DataType)
        return super().__new__(DataType, f'{DataType.__name__}T', (Data,), {
            '__pakkit_fromstream__': classmethod(DataType.__pakkit_fromstream__)
        })
    def __pakkit_fromstream__(self, stream):
        raise NotImplementedError()

# class SimpleData(Data):


# def instancemethod(f):
#     return f

class Array(DataType):
    def __init__(ArrayT, dtype, size=...):
        print('ARRAY INIT', dtype, size)
        ArrayT.dtype = dtype
        ArrayT.size = size
    def __pakkit_fromstream__(self, stream):
        print('ARRAY FROMSTREAM', self, stream)
        return stream


ArrayType = Array[int, 8]

print(ArrayType.__pakkit_fromstream__('govnostream'))
