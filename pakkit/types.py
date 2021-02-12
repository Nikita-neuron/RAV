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
    def from_stream(cls, stream):
        raise NotImplementedError()
    def to_stream(self, stream):
        raise NotImplementedError()


class DataTypeMeta(type):
    def __getitem__(self, args):
        if type(args) == tuple:
            return self(*args)
        return self(args)



class DataType(type, metaclass=DataTypeMeta):
    # *args и **kwargs - аргументы для подклассов, они тут как заглушка
    def __new__(DataType, name, bases, d: dict):
        # print('DATATYPE NEW', DataType)
        # d = kwargs.get('d', {
        #     '__pakkit_fromstream__': classmethod(DataType.__pakkit_fromstream__),
        # })
        # for name, value in DataType.__dict__.items():
        #     if name.startswith('instance_'):
        #         d[name[len('instance_'):]] = value
        #     elif name.startswith('__instance_'):
        #         d['__'+name[len('__instance_'):]] = value
        class T(Data):
            pass
            # @classmethod
            # def from_stream(cls, stream: typing.BinaryIO):
            #     raise NotImplementedError()
        return T
        # return super().__new__(DataType, DataType.__name__, (Data,), d)
    


class SimpleData(DataType):
    def __new__(SimpleData, ctype, name):
        class T(Data):
            __ctype = ctype
            def __init__(self, value = 0):
                self.__cdata = self.__ctype(value)
            @classmethod
            def from_stream(cls, stream):
                self = cls()
                self.__cdata = self.__ctype.from_buffer_copy(stream.read(sizeof(self.__ctype)))
                return self
            @property
            def value(self):
                return self.__cdata.value
            def __str__(self):
                return str(self.value)
            def __repr__(self):
                return f'{self.__class__.__name__}({self})'
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

# class SimpleData(Data):


# def instancemethod(f):
#     return f

class Array(DataType):
    # def __init__(ArrayT, dtype, size=...):
    #     ArrayT.dtype = dtype
    #     ArrayT.size = size if size is ... else size_t(size)
    def __new__(Array, dtype, size=...):
        class T(Data):
            __dtype = dtype
            __size = size if size is ... else size_t(size)
            def __init__(self):
                self.__data = None
            @classmethod
            def from_list(cls, lst: list):
                self = cls()
                # TODO: Глубокое копирование lst и автоматическое конструирование dtype'ов
                self.__data = lst.copy()
                return self
            @classmethod
            def from_stream(cls, stream):
                self = cls()
                if self.__size is ...:
                    size = size_t.from_buffer_copy(stream.read(sizeof(size_t)))
                else:
                    size = self.__size
                self.__data = []
                for _ in range(size.value):
                    self.__data.append(self.__dtype.from_stream(stream))
                return self
            def __len__(self):
                return len(self.__data)
            def __iter__(self):
                return iter(self.__data)
            def __repr__(self):
                return f'{self.__class__.__name__}{{{", ".join(map(str, self))}}}'
        T.__name__ = T.__qualname__ = f'Array[{dtype.__name__}, {size}]'
        return T


class StructType(DataType):
    def __new__(StructType, name, bases, d: dict):
        fields = d.get('__pakkit_fields__', {})
        print('StructType new', StructType, name, bases, d)
        if '__annotations__' in d:
            for name, dtype in d['__annotations__'].items():
                print(name, dtype)
                if issubclass(dtype, Data):
                    fields[name] = dtype
        class T(Data):
            __pakkit_fields__ = fields
            @classmethod
            def from_stream(cls, stream):
                self = cls()
                for name, dtype in cls.__pakkit_fields__.items():
                    self.__dict__[name] = dtype.__pakkit_fromstream__(stream)
                return self
            def to_stream(self, stream):
                for name in self.__pakkit_fields__:
                    self.__dict__[name].to_stream(stream)
        T.__name__ = T.__qualname__ = 'FSFFSSFSTARACT'
        return T
    # def __instance_repr__(self)
class Struct(metaclass=StructType):
    pass
class MyStruct(Struct):
    num: i32
    array_static: Array[i8, 4]
    array_dynamic: Array[i8, ...]

def main():
    import io


    # stream_in = io.BytesIO(b'\x04\x03\x02\x01')
    # print(Array[u8, 4].from_stream(stream_in))

    #                        #               #               #
    stream_in = io.BytesIO(b'\x01\x00\x00\x00\x01\x02\x03\x04\x05\x00\x00\x00\x05\x04\x03\x02\x01')
    stream_out = io.BytesIO()
    # MyStruct.__pakkit_fromstream__(stream_in)
    s = MyStruct.from_stream(stream_in)
    s.to_stream(stream_out)
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