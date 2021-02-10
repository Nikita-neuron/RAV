
class DataType(type):
    pass
    # def __new__(Array, *args, **kwargs):
    #     return super

class Array(DataType):
    def __new__(Array, dtype):
        print('ARRAY NEW', Array, dtype)
        def wr(stream):
            return Array.__pakkit_fromstream__(result(), stream)
        result = super().__new__(Array, 'ArrayT', (), {'__pakkit_fromstream__': classmethod(sel)})
        
        return result
    def __pakkit_fromstream__(self, stream):
        print('ARRAY FROMSTREAM', self, stream)
        return stream
        # self.data = 
    # def __call__(self, *args, **kwargs):
    #     print('ARRAY CALL', args, kwargs)
    # def __init__(self, dtype):
    #     # print('ARRAY NEW', Array, name, bases, d)
    #     print('ARRAY INIT', self, dtype)
    #     return super().__new__(Array, self.__name__, (), {})
    pass


ArrayType = Array(int)
print(ArrayType.__pakkit_fromstream__('govnostream'))
