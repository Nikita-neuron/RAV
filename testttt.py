
def decor(f):
    print('DECOR', f)
    return f

class MetaClass(type):
    @decor
    def func(self):
        print('FUNC', self)

class Class(metaclass=MetaClass):
    pass

Class.func()
print(Class.func)

