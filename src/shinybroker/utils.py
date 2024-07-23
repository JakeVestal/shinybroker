import struct


def pack_element(msg_emt) -> str:
    match type(msg_emt).__name__:
        case 'str':
            return msg_emt + "\0"
        case 'NoneType':
            raise ValueError("Cannot send None to a message function")
        case 'bool':
            return str(int(msg_emt)) + "\0"
        case _:
            return str(msg_emt) + "\0"


def pack_message(msg_txt) -> bytes:
    return struct.pack(
        f"!I{len(msg_txt)}s",
        len(msg_txt),
        str.encode(msg_txt)
    )
