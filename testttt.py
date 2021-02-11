import pakkit
from pakkit.types import (u8, Array)
import io

stream = io.BytesIO(b'\x00\x01\x02\x03')
# ArrayType = Array[u8, 4]
# print(ArrayType.__pakkit_fromstream__())
print(u8.__pakkit_fromstream__(stream).cdata)

