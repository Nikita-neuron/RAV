import ctypes
from ctypes import (
    c_int8, c_uint8,
    c_int16, c_uint16,
    c_int32, c_uint32,
    c_int64, c_uint64,
    sizeof
)
import array
import typing


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



class DataType(type, metaclass=DataTypeMeta):
    # *args и **kwargs - аргументы для подклассов, они тут как заглушка
    def __new__(DataType):
        # print('DATATYPE NEW', DataType)
        # d = kwargs.get('d', {
        #     '__pakkit_fromstream__': classmethod(DataType.__pakkit_fromstream__),
        # })
        # for name, value in DataType.__dict__.items():
        #     if name.startswith('instance_'):
        #         d[name[len('instance_'):]] = value
        #     elif name.startswith('__instance_'):
        #         d['__'+name[len('__instance_'):]] = value
        class T(type, Data):
            @classmethod
            def __pakkit_fromstream__(cls, stream: typing.BinaryIO):
                raise NotImplementedError()
        return T
        # return super().__new__(DataType, DataType.__name__, (Data,), d)
    


class SimpleData(DataType):
    def __new__(SimpleData, ctype, name):
        print('NEW', SimpleData, ctype, name)
        class T(Data):
            __ctype = ctype
            def __init__(self, value):
                self.__cdata = self.__ctype(value)
            @classmethod
            def __pakkit_fromstream__(cls, stream):
                self = cls()
                self.__cdata = self.__ctype.from_buffer_copy(stream.read(sizeof(self.__ctype)))
                return self
            @property
            def value(self):
                return self.__cdata.value
        T.__name__ = T.__qualname__ = name
        return T
    # def __init__(self, ctype, name):
    #     self.__name__ = name
    #     self._ctype = ctype
    # @property
    # def instance_value(self):
    #     return self.cdata.value
    # def __instance_init__(self, value=0):
    #     self.cdata = self._ctype(value)
    # def __pakkit_fromstream__(cls, stream):
    #     pass
    # def __instance_pakkit_tostream__(self, stream):
    #     stream.write(self.cdata)
    # def __repr__(cls):
    #     return f'{cls.__name__}'
    # def __instance_str__(self):
    #     return f'{self.value}'
    # def __instance_repr__(self):
    #     return f'{type(self)}({self.value})'

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

size_t = ctypes.c_uint32

if __name__ == "__main__":
    print(i8)
