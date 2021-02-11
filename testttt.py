

class Data:
    pass

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
