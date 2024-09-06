import select
import shinybroker as sb


ib_socket, API_VERSION, CONNECTION_TIME = sb.create_ibkr_socket_conn(
    client_id=9999
)

(rd, wt, er) = select.select([], [ib_socket], [])
wt[0].send(
    sb.req_sec_def_opt_params(
        reqId=1,
        underlyingSymbol="AAPL",
        futFopExchange="",
        underlyingSecType="STK",
        underlyingConId=265598
    )
)

while True:
    incoming_msg = sb.read_ib_msg(sock=ib_socket)
    print(incoming_msg)
    if incoming_msg[0] == sb.functionary['incoming_msg_codes'][
        'SECURITY_DEFINITION_OPTION_PARAMETER'
    ]:
        sdop = sb.format_sec_def_opt_params_input(sdop=incoming_msg[1:])
        break




