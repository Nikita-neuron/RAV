
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
    def __new__(DataType, *args, **kwargs):
        # print('DATATYPE NEW', DataType)
        d = kwargs.get('d', {
            '__pakkit_fromstream__': classmethod(DataType.__pakkit_fromstream__),
        })
        for name, value in DataType.__dict__.items():
            if name.startswith('instance_'):
                d[name[len('instance_'):]] = value
            elif name.startswith('__instance_'):
                d['__'+name[len('__instance_'):]] = value
        
        return super().__new__(DataType, DataType.__name__, (Data,), d)
    def __pakkit_fromstream__(cls, stream: typing.BinaryIO):
        raise NotImplementedError()
    def __instance_pakkit_fromstream__(cls, stream: typing.BinaryIO):
        raise NotImplementedError()
    

class SimpleData(DataType):
    def __init__(self, ctype, name):
        self.__name__ = name
        self._ctype = ctype
    @property
    def instance_value(self):
        return self.cdata.value
    def __instance_init__(self, value=0):
        self.cdata = self._ctype(value)
    def __pakkit_fromstream__(cls, stream):
        self = cls()
        self.cdata = self._ctype.from_buffer_copy(stream.read(sizeof(self._ctype)))
        return self
    def __instance_pakkit_tostream__(self, stream):
        stream.write(self.cdata)
    def __repr__(cls):
        return f'{cls.__name__}'
    def __instance_str__(self):
        return f'{self.value}'
    def __instance_repr__(self):
        return f'{type(self)}({self.value})'

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

# class SimpleData(Data):


# def instancemethod(f):
#     return f

class Array(DataType):
    def __init__(ArrayT, dtype, size=...):
        ArrayT.dtype = dtype
        ArrayT.size = size if size is ... else size_t(size)
    def __pakkit_fromstream__(cls, stream):
        self = cls()
        if self.size is ...:
            size = size_t.from_buffer_copy(stream.read(sizeof(size_t)))
        else:
            size = self.size
        self.__data = []
        for _ in range(size.value):
            self.__data.append(self.dtype.__pakkit_fromstream__(stream))
        return self
    def __instance_pakkit_tostream__(self, stream):
        if self.size is ...:
            stream.write(size_t(len(self.__data)))
        for value in self.__data:
            value.__pakkit_tostream__(stream)
        
    def instance_as_list(self):
        return self.__data[:]
    def instance_iter(self):
        return self.as_list()
    def __repr__(cls):
        return f'{cls.__name__}[{cls.dtype}, {cls.size}]'
    def __instance_repr__(self):
        s = ', '.join(map(lambda v: str(v), self.as_list()))
        return f'{type(self)}{{{s}}}'

class StructType(DataType):
    def __init__(Struct, name, bases, d: dict):
        fields = d.get('__pakkit_fields__', {})
        print('new', Struct, name, bases, d)
        if '__annotations__' in d:
            for name, dtype in d['__annotations__'].items():
                if issubclass(dtype, Data):
                    fields[name] = dtype
        Struct.__pakkit_fields__ = fields
    def __pakkit_fromstream__(cls, stream):
        self = cls()
        for name, dtype in cls.__pakkit_fields__.items():
            self.__dict__[name] = dtype.__pakkit_fromstream__(stream)
        return self
    def __instance_pakkit_tostream__(self, stream):
        for name in self.__pakkit_fields__:
            self.__dict__[name].__pakkit_tostream__(stream)
    def __instance_repr__(self)
class Struct(metaclass=StructType):
    pass
class MyStruct(Struct):
    num: i32
    array_static: Array[i8, 4]
    array_dynamic: Array[i8, ...]

def main():
    import io
    #                        #               #               #
    stream_in = io.BytesIO(b'\x01\x00\x00\x00\x01\x02\x03\x04\x05\x00\x00\x00\x05\x04\x03\x02\x01')
    stream_out = io.BytesIO()
    # MyStruct.__pakkit_fromstream__(stream_in)
    s = MyStruct.__pakkit_fromstream__(stream_in)
    s.__pakkit_tostream__(stream_out)
    print(s.array_dynamic)

    # stream_in = io.BytesIO(b'\x00\x01\x02\x03')
    # t = Array[u8, 4]
    # arr = t.__pakkit_fromstream__(stream_in)
    # print(arr)
    # stream_out = io.BytesIO()
    # arr.__pakkit_tostream__(stream_out)
    # print('v', stream_out.getvalue())


if __name__ == '__main__':
    main()
