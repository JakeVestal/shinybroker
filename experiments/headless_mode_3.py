from collections import deque
from threading import Thread, Event
from time import sleep
import shinybroker as sb


ib_socket, API_VERSION, CONNECTION_TIME = sb.create_ibkr_socket_conn()

event = Event()


def add_msg_to_queue(sock_conn, queue):
    while True:
        msg = sb.read_ib_message(s=sock_conn)
        print('msg received:', msg)
        queue.append(msg)
        if event.is_set():
            break
    sock_conn.close()


q = deque()
t = Thread(
    target=add_msg_to_queue,
    kwargs={
        'sock_conn': ib_socket,
        'queue': q
    }
)
t.start()

while True:
    try:
        sleep(.5)
    except KeyboardInterrupt:
        event.set()
        break
t.join()
print(q)



# ib_msg_reader_thread = Thread(
#     target=sb.ib_msg_reader_run_loop,
#     kwargs={'ib_sock': ib_socket, 'verbose': True}
# )
# ib_msg_reader_thread.start()
#
# # Make a request for TRADES on AAPL stock every five minutes over the past hour

#
# # Make a request for the options parameters on AAPL
# sb.send_ib_message(
#     s=ib_socket,
#     msg=sb.req_sec_def_opt_params(
#         reqId=1,
#         underlyingSymbol="AAPL",
#         underlyingSecType="STK",
#         underlyingConId=265598
#     )
# )




# import select
# import shinybroker as sb
#
#
# ib_socket, API_VERSION, CONNECTION_TIME = sb.create_ibkr_socket_conn()
#
# (rd, wt, er) = select.select([], [ib_socket], [])
# wt[0].send(
#     sb.req_sec_def_opt_params(
#         reqId=1,
#         underlyingSymbol="AAPL",
#         futFopExchange="",
#         underlyingSecType="STK",
#         underlyingConId=265598
#     )
# )
#
# while True:
#     incoming_msg = sb.read_ib_msg(sock=ib_socket)
#     print(incoming_msg)
#     if incoming_msg[0] == sb.functionary['incoming_msg_codes'][
#         'SECURITY_DEFINITION_OPTION_PARAMETER'
#     ]:
#         sdop = sb.format_sec_def_opt_params_input(sdop=incoming_msg[1:])
#         break



# ib_msg_reader_thread = Thread(
#     target=sb.ib_msg_reader_run_loop,
#     kwargs={'ib_sock': ib_socket, 'verbose': True}
# )
# ib_msg_reader_thread.start()
#
# # Make a request for TRADES on AAPL stock every five minutes over the past hour

#
# # Make a request for the options parameters on AAPL
# sb.send_ib_message(
#     s=ib_socket,
#     msg=sb.req_sec_def_opt_params(
#         reqId=1,
#         underlyingSymbol="AAPL",
#         underlyingSecType="STK",
#         underlyingConId=265598
#     )
# )




# import select
# import shinybroker as sb
#
#
# ib_socket, API_VERSION, CONNECTION_TIME = sb.create_ibkr_socket_conn()
#
# (rd, wt, er) = select.select([], [ib_socket], [])
# wt[0].send(
#     sb.req_sec_def_opt_params(
#         reqId=1,
#         underlyingSymbol="AAPL",
#         futFopExchange="",
#         underlyingSecType="STK",
#         underlyingConId=265598
#     )
# )
#
# while True:
#     incoming_msg = sb.read_ib_msg(sock=ib_socket)
#     print(incoming_msg)
#     if incoming_msg[0] == sb.functionary['incoming_msg_codes'][
#         'SECURITY_DEFINITION_OPTION_PARAMETER'
#     ]:
#         sdop = sb.format_sec_def_opt_params_input(sdop=incoming_msg[1:])
#         break

