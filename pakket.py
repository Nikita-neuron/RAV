
import ctypes
from ctypes import (
    c_int8, c_uint8,
    c_int16, c_uint16,
    c_int32, c_uint32,
    c_int64, c_uint64,
)

i8 = c_int8; u8 = c_uint8
i16 = c_int16; u16 = c_uint16
i32 = c_int32; u32 = c_uint32
i64 = c_int64; u64 = c_uint64

class StructMeta(type):
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        super().__init__(*args, **kwargs)

class Struct(metaclass = StructMeta):
    pass
