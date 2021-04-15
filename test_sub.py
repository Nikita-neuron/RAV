
import traceback

old_print = print
def spy_print(*args, **kwargs):
    frame = traceback.extract_stack()[-2]
    old_print(f'[{frame.name}]', *args, **kwargs)
print = spy_print

print('Hello, World')

