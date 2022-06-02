from typing import Any, Literal, Tuple, Union

def read_int(
    content: list,
    addr: int,
    size: int,
    endian: Literal["little", "big"] = "little",
    signed: bool = False,
) -> int:
    return int.from_bytes(content[addr:addr+size], byteorder=endian, signed=signed)
