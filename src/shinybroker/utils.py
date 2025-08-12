import struct
import datetime

import pandas as pd


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

def formatter2(hrs_str):

    z = [y.split("-") for y in [x for x in hrs_str.split(";")]]

    for i in range(len(z)):
        if len(z[i]) == 1 and z[i][0].split(":")[1] == 'CLOSED':
            z[i] = [z[i][0], z[i][0]]

    df = pd.merge(
        pd.DataFrame(
            data={
                "end_time": [a[1].split(":")[1] for a in z]
            },
            index=[datetime.datetime.strptime(x, "%Y%m%d").date() for x in
                   [a[1].split(":")[0] for a in z]]
        ),
        pd.DataFrame(
            data = {
                "start_time": [a[0].split(":")[1] for a in z]
            },
            index = [datetime.datetime.strptime(x, "%Y%m%d").date() for x in
                     [a[0].split(":")[0] for a in z]]
        ),
        left_index=True,
        right_index=True,
        how="outer"
    )

    df = df.fillna('')

    return df
