
# def decor(f):
#     print('DECOR', f)
#     return f

class MegaMeta(type)

class MetaClass(type):
    def __new__(cls, name):
        class T:
            def f(self):
                print('Hello!')
        T.__name__ = name
        print(T.__dict__['f'].)
        return T
# class Class(metaclass=MetaClass):
#     pass

Class = MetaClass('Class')
Class().f()

