import struct


def pack_message(msg_txt) -> bytes:
    return struct.pack(
        f"!I{len(msg_txt)}s",
        len(msg_txt),
        str.encode(msg_txt)
    )
