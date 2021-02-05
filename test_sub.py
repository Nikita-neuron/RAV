
import sys

class ReprFile:
    def write(self, data):
        print(repr(data))
print('', file=ReprFile())
