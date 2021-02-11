
import ctypes
from ctypes import (
    c_int8, c_uint8,
    c_int16, c_uint16,
    c_int32, c_uint32,
    c_int64, c_uint64,
)


# _CData = i8.__base__.__base__
# _PyCStructType = ctypes.Structure.__class__

class Data:
    @classmethod
    def __pakkit_fromstream__(cls, stream):
        raise NotImplementedError()


class DataTypeMeta(type):
    def __getitem__(self, args):
        if type(args) == tuple:
            return self(*args)
        return self(args)

def instancemethod

class DataType(type, metaclass=DataTypeMeta):
    # *args и **kwargs - аргументы для подклассов, они тут как заглушка
    def __new__(DataType, *args, **kwargs):
        # print('DATATYPE NEW', DataType)
        return super().__new__(DataType, f'{DataType.__name__}T', (Data,), {
            '__pakkit_fromstream__': classmethod(DataType.__pakkit_fromstream__)
        })
    def __pakkit_fromstream__(self, stream):
        raise NotImplementedError()


class SimpleData(DataType):
    def __init__(self, ctype, name):
        self.__name__ = name
        self._ctype = ctype
    def __pakkit_fromstream__(cls, stream):
        print('FROMSTREAM', cls, stream)
        self = cls()
        self.cdata = self._ctype.from_buffer_copy(stream.read(ctypes.sizeof(self._ctype)))
        return self

i8:  SimpleData; u8:  SimpleData
i16: SimpleData; u16: SimpleData
i32: SimpleData; u32: SimpleData
i64: SimpleData; u64: SimpleData

for name, ctype in dict(
        i8 = c_int8,   u8 = c_uint8,
        i16 = c_int16, u16 = c_uint16,
        i32 = c_int32, u32 = c_uint32,
        i64 = c_int64, u64 = c_uint64).items():
    globals()[name] = SimpleData(ctype, name)


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


