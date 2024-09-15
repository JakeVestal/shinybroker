# import shinybroker as sb
# import pandas as pd
#
#
# con_id = 265598  # AAPL Stock
#
#
# ib_conn = sb.create_ibkr_socket_conn()
# ib_socket = ib_conn['ib_socket']
#
# sb.send_ib_message(
#     s=ib_socket,
#     msg=sb.req_sec_def_opt_params(
#         reqId=1,
#         underlyingSymbol="AAPL",
#         futFopExchange="",
#         underlyingSecType="STK",
#         underlyingConId=265598
#     )
# )
#
# # start_time = datetime.datetime.now()
# # while (datetime.datetime.now() - start_time).seconds < timeout:
# incoming_msg = sb.read_ib_msg(sock=ib_socket)
# sdops = []
# while incoming_msg[0] != sb.functionary['incoming_msg_codes'][
#     'SECURITY_DEFINITION_OPTION_PARAMETER_END'
# ]:
#     incoming_msg = sb.read_ib_msg(sock=ib_socket)
#     if incoming_msg[0] == sb.functionary['incoming_msg_codes'][
#         'SECURITY_DEFINITION_OPTION_PARAMETER'
#     ]:
#     sdops.append(sb.format_sec_def_opt_params_input(sdop=incoming_msg[2:]))
#
# ib_socket.close()
#
#
# print(
#     pd.concat(sdops, ignore_index=True)
#     .sort_values('exchange')
# )
