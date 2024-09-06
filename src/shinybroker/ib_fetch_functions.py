from shinybroker.connection import (
    create_ibkr_socket_conn, send_ib_message, read_ib_msg
)
from shinybroker.functionary import functionary
from shinybroker.msgs_to_ibkr import req_sec_def_opt_params
from shinybroker.format_ibkr_inputs import *


def fetch_sec_def_opt_params(
        underlyingConId: int,
        underlyingSymbol: str,
        underlyingSecType: str,
        host='127.0.0.1',
        port=7497,
        client_id=9999,
        futFopExchange="",
        timeout=3
):
    ib_conn = create_ibkr_socket_conn(
        host=host, port=port, client_id=client_id
    )
    ib_socket = ib_conn['ib_socket']

    send_ib_message(
        s=ib_socket,
        msg=req_sec_def_opt_params(
            reqId=ib_conn['NEXT_VALID_ID'],
            underlyingSymbol=underlyingSymbol,
            futFopExchange=futFopExchange,
            underlyingSecType=underlyingSecType,
            underlyingConId=underlyingConId
        )
    )

    print('handle inf while loop timeout')
    print('handle timeout on socket')

    # start_time = datetime.datetime.now()
    # while (datetime.datetime.now() - start_time).seconds < timeout:
    incoming_msg = read_ib_msg(ib_socket)
    sdops = []
    while incoming_msg[0] != functionary['incoming_msg_codes'][
        'SECURITY_DEFINITION_OPTION_PARAMETER_END'
    ]:
        incoming_msg = read_ib_msg(sock=ib_socket)
        if incoming_msg[0] == functionary['incoming_msg_codes'][
            'SECURITY_DEFINITION_OPTION_PARAMETER'
        ]:
            sdops.append(
                format_sec_def_opt_params_input(sdop=incoming_msg[2:]))

    ib_socket.close()

    return pd.concat(sdops, ignore_index=True).sort_values('exchange')


