import threading, select
import shinybroker as sb


ib_socket, API_VERSION, CONNECTION_TIME = sb.create_ibkr_socket_conn()

ib_msg_reader_thread = threading.Thread(
    target=sb.ib_msg_reader_run_loop,
    kwargs={'ib_sock': ib_socket, 'verbose': True}
)
ib_msg_reader_thread.start()


(rd, wt, er) = select.select([], [ib_socket], [])
wt[0].send(
    sb.req_historical_data(
        reqId=1,
        contract=sb.Contract({
            'symbol': "AAPL",
            'secType': "STK",
            'exchange': "SMART",
            'currency': "USD"
        }),
        durationStr="1 W",
        keepUpToDate=0
    )
)


(rd, wt, er) = select.select([], [ib_socket], [])
wt[0].send(
    sb.req_sec_def_opt_params(
        reqId=1,
        underlyingSymbol="AAPL",
        underlyingSecType="STK",
        underlyingConId=265598
    )
)

