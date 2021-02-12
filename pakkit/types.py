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


_CData = c_uint8.__base__.__base__
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
    def __new__(DataType, name, bases, d: dict):
        bases = bases if Data in bases else bases+(Data,)
        return super().__new__(DataType, name, bases, d)


class SimpleData(DataType):
    def __new__(SimpleData, name, bases, d: dict, ctype=...):
        '''
        Создаёт новый тип из данного ctype:
            1) Если ctype - тип из 'ctypes'(подкласс _CData), ничего особенного не происходит.
            2) Если ctype == ..., ищет наследников SimpleData в bases, берёт первого попавшегося и получает _ctype оттуда.
            3) Если не найдены подходящие наследники или ctype какого-то другого типа, вызывается ошибка
        '''
        found_ctype = False
        if ctype is ...:
            for base in bases:
                if isinstance(base, SimpleData):
                    ctype = base._ctype
                    found_ctype = True
                    break
        elif issubclass(ctype, _CData):
            found_ctype = True
        if not found_ctype:
            raise TypeError(f'Неправильный тип ctype ({ctype}) или не найдены наследники SimpleDataT')

        class T(Data):
            _ctype = ctype
            def __init__(self, value = 0):
                self._cdata = self._ctype(value)
            @classmethod
            def from_stream(cls, stream):
                self = cls()
                self._cdata = self._ctype.from_buffer_copy(stream.read(sizeof(self._ctype)))
                return self
            def to_stream(self, stream):
                stream.write(self._cdata)
            @property
            def value(self):
                return self._cdata.value
            def __str__(self):
                return str(self.value)
            def __repr__(self):
                return f'{self.__class__.__name__}({self})'
        T.__name__ = T.__qualname__ = name
        return super().__new__(SimpleData, name, (), dict(T.__dict__))
    def __init__(SimpleDataT, name, bases, d: dict, ctype=...):
        pass
    
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

def __create_basic_types():
    ''' Создаёт базовые целочисленные типы в глобальном пространстве имён. '''
    for name, ctype in dict(
            i8 = c_int8,   u8 = c_uint8,
            i16 = c_int16, u16 = c_uint16,
            i32 = c_int32, u32 = c_uint32,
            i64 = c_int64, u64 = c_uint64).items():
        globals()[name] = SimpleData(name, (), {}, ctype)
__create_basic_types()

size_t = ctypes.c_uint32

# class SimpleData(Data):


# def instancemethod(f):
#     return f

class Array(DataType):
    def __new__(Array, dtype, size=...):
        class T(Data):
            _dtype = dtype
            _size = size if size is ... else size_t(size)
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
                if self._size is ...:
                    size = size_t.from_buffer_copy(stream.read(sizeof(size_t)))
                else:
                    size = self._size
                self.__data = []
                for _ in range(size.value):
                    self.__data.append(self._dtype.from_stream(stream))
                return self
            def to_stream(self, stream):
                if self._size is ...:
                    stream.write(size_t(len(self)))
                for val in self.__data:
                    val.to_stream(stream)
            def __len__(self):
                return len(self.__data)
            def __iter__(self):
                return iter(self.__data)
            def __repr__(self):
                return f'{self.__class__.__name__}{{{", ".join(map(str, self))}}}'
        return super().__new__(
            Array,
            f'Array[{dtype.__name__}, {"..." if size is ... else size}]',
            (),
            dict(T.__dict__))
    
    def __init__(self, *args, **kwargs):
        pass


class StructType(DataType):
    def __new__(StructType, name, bases, d: dict):
        fields = d.get('__pakkit_fields__', {})
        if '__annotations__' in d:
            for annot_name, dtype in d['__annotations__'].items():
                if issubclass(dtype, Data):
                    fields[annot_name] = dtype
        class T(Data):
            __pakkit_fields__ = fields
            @classmethod
            def from_stream(cls, stream):
                self = cls()
                for name, dtype in cls.__pakkit_fields__.items():
                    self.__dict__[name] = dtype.from_stream(stream)
                return self
            def to_stream(self, stream):
                for name in self.__pakkit_fields__:
                    self.__dict__[name].to_stream(stream)
            def __repr__(self):
                return (
                    f'{self.__class__.__name__} {{\n\t'
                    + ',\n\t'.join((f'{name} = {repr(self.__dict__[name])}' for name in self.__pakkit_fields__))
                    + '\n}'
                )
        return super().__new__(StructType, name, bases, T.__dict__ | d)


# Struct и так по умолчанию наследник Data, но VSCode этого не понимает...
class Struct(Data, metaclass=StructType):
    pass


# class EnumValue(Data):
#     pass
class EnumType(DataType):
    def __new__(EnumType, name, bases, d: dict, dtype=u16):
        next_value = 0
        for field_name, value in d.items():
            if value is ...:
                value = next_value
                next_value += 1
            elif type(value) == int:
                next_value = value+1
            else:
                continue
            d[field_name] = dtype(value)
        return super().__new__(EnumType, name, bases, d)
class Enum(metaclass=EnumType):
    pass




def _test_struct():
    import io

    class MyStruct(Struct):
        num: i32
        array_static: Array[i8, 4]
        array_dynamic: Array[i8, ...]

    #                       <| num           | array_static  | [size]        | array_dynamic     >
    stream_in = io.BytesIO(b'\x01\x00\x00\x00\x01\x02\x03\x04\x05\x00\x00\x00\x05\x04\x03\x02\x01')
    stream_out = io.BytesIO()
    s = MyStruct.from_stream(stream_in)
    s.to_stream(stream_out)
    print(s, stream_out.getvalue())
    assert stream_in.getvalue() == stream_out.getvalue()

def _test_enum():
    import sys
    
    class MyEnum(Enum, dtype=u8):
        A = ... # 0
        B = 3
        C = ... # ==4
        D = ... # ==5
        E = 100
        F = ... # 101
    for attr_name in ('A', 'B', 'C', 'D', 'E', 'F'):
        print(f'MyEnum.{attr_name} = {getattr(MyEnum, attr_name)}')

def main():
    _test_enum()

if __name__ == '__main__':
    main()