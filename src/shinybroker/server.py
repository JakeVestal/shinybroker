import datetime
import json
import select
import sys
import threading

import pandas as pd

from io import StringIO
from shinybroker.connection import (
    create_ibkr_socket_conn, ib_msg_reader_run_loop
)
from shinybroker.msgs_to_ibkr import *
from shiny import Inputs, Outputs, Session, reactive

def sb_server(input: Inputs, output: Outputs, session: Session):

    ib_socket, API_VERSION, CONNECTION_TIME = create_ibkr_socket_conn(
        client_id=10645
    )
    session.on_ended(ib_socket.close)

    print(
        'Connected to IBKR at ' + CONNECTION_TIME +
        ' under API protocol version ' + API_VERSION
    )

    # Creates a thread object for the async function that reads incoming
    #   messages from the socket
    # Passes to that function:
    #   - the socket connection
    #   - the Shiny session
    # Starts the thread
    ib_msg_reader_thread = threading.Thread(
        target=rxt.ib_msg_reader_run_loop,
        kwargs={
            'ib_sock': ib_socket,
            'shiny_sesh': session,
            'verbose': True
        }
    )
    ib_msg_reader_thread.start()

    # Market Data Type
    # When input.market_data_type is set / changed by the user via the
    #   sidebar radio buttons, Shiny send the corresponding setting to IBKR.
    # When market data arrives from the socket, IBKR reports what type of
    #   market data (delayed, live, etc.) it is. Shiny stores that latest value
    #   in input.market_data_type.

    market_data_type = reactive.value()

    @reactive.effect
    @reactive.event(input.market_data_type)
    def request_market_data_type():
        (rd, wt, er) = select.select([], [ib_socket], [])
        wt[0].send(req_market_data_type(input.market_data_type()))

    @reactive.effect
    @reactive.event(input.market_data_type)
    def update_market_data_type():
        market_data_type.set(input.market_data_type())

    # @render.text
    # def market_data_type_txt():
    #
    #     match market_data_type():
    #         case "1":
    #             mdt = "1: Live"
    #         case "2":
    #             mdt = "2: Frozen"
    #         case "3":
    #             mdt = "3: Delayed"
    #         case "4":
    #             mdt = "4: Delayed Frozen"
    #         case _:
    #             mdt = market_data_type()
    #
    #     return "Received Mkt Data Type " + mdt
    #
    # # Managed Accounts
    #
    # managed_accounts = reactive.value([])
    #
    # @reactive.effect
    # @reactive.event(input.managed_accounts)
    # def update_managed_accounts():
    #     managed_accounts.set(list(input.managed_accounts())[1:])
    #
    # # Next Valid ID
    #
    # next_valid_id = reactive.value()
    #
    # @reactive.effect
    # @reactive.event(input.next_valid_id)
    # def update_next_valid_id():
    #     next_valid_id.set(str(input.next_valid_id()[1]))
    #
    # @render.text
    # def next_valid_id_txt():
    #     return "Next Valid ID: " + next_valid_id()
    #
    # # Error Messages
    #
    # error_messages = reactive.value(
    #     pd.DataFrame(
    #         columns=["error_id", "error_code", "error_message"],
    #         index=None
    #     )
    # )
    #
    # @reactive.effect
    # @reactive.event(input.error_message)
    # def update_error_messages():
    #     err_msgs = error_messages()
    #     new_msg = input.error_message()
    #     error_messages.set(
    #         pd.concat(
    #             [
    #                 err_msgs,
    #                 pd.DataFrame(
    #                     {
    #                         "error_id": new_msg[1],
    #                         "error_code": new_msg[2],
    #                         "error_message": new_msg[3]
    #                     },
    #                     index=[len(err_msgs)]
    #                 )
    #             ],
    #             axis=0
    #         )
    #     )
    #
    # @render.table
    # def error_messages_df():
    #     return error_messages().style.set_table_attributes(
    #         'class="dataframe shiny-table table w-auto"'
    #     ).hide(axis="index")
    #
    # @reactive.effect
    # @reactive.event(input.error_notification)
    # def send_error_message_notification():
    #     ui.notification_show(input.error_notification())
    #
    # # Current Time
    # # Useful mostly just to check if i/o is working.
    # # Runs when the user clicks the req_current_time button and updates the
    #
    # current_time = reactive.value()
    #
    # @reactive.effect
    # @reactive.event(input.req_current_time, ignore_init=True)
    # def request_current_time():
    #     (rd, wt, er) = select.select([], [ib_socket], [])
    #     wt[0].send(rxt.req_current_time())
    #
    # @reactive.effect
    # @reactive.event(input.current_time)
    # def update_current_time():
    #     current_time.set(
    #         str(datetime.datetime.fromtimestamp(int(input.current_time()[1])))
    #     )
    #
    # @render.text
    # def current_time_txt():
    #     return current_time()
    #
    # # Matching Symbols #########################################################
    #
    # matching_symbols = reactive.value()
    #
    # @reactive.effect
    # @reactive.event(input.req_matching_symbols)
    # def request_matching_symbols():
    #     (rd, wt, er) = select.select([], [ib_socket], [])
    #     wt[0].send(
    #         rxt.req_matching_symbols(
    #             reqId=next_valid_id(),
    #             pattern=input.requested_symbol()
    #         )
    #     )
    #
    # @reactive.effect
    # @reactive.event(input.symbol_samples)
    # def update_matching_symbols():
    #
    #     symbol_samples = list(input.symbol_samples())[2:]
    #
    #     bonds = rxt.initial_rx_values['matching_symbols']['bonds']
    #
    #     while True:
    #         try:
    #             bond_ind = symbol_samples.index('-1')
    #             bonds = pd.concat(
    #                 [
    #                     bonds,
    #                     pd.DataFrame.from_dict({
    #                         'issuer': [symbol_samples[bond_ind + 3]],
    #                         'issuer_id': [symbol_samples[bond_ind + 4]]
    #                     })
    #                 ],
    #                 ignore_index=True
    #             )
    #             del symbol_samples[bond_ind:bond_ind + 5]
    #         except ValueError:
    #             break
    #
    #     ui.update_switch(id='show_matching_bonds', value=bonds.shape[0] > 0)
    #
    #     stocks = rxt.initial_rx_values['matching_symbols']['stocks']
    #
    #     while True:
    #         try:
    #             n_derivative_contracts = int(symbol_samples[5])
    #             stocks = pd.concat(
    #                 [
    #                     stocks,
    #                     pd.DataFrame.from_dict({
    #                         'con_id': [symbol_samples[0]],
    #                         'symbol': [symbol_samples[1]],
    #                         'sec_type': [symbol_samples[2]],
    #                         'primary_exchange': [symbol_samples[3]],
    #                         'currency': [symbol_samples[4]],
    #                         'derivative_sec_types': ",".join(
    #                             symbol_samples[6:5 + n_derivative_contracts]
    #                         ),
    #                         'description': [
    #                             symbol_samples[6 + n_derivative_contracts]]
    #                     })
    #                 ],
    #                 ignore_index=True
    #             )
    #             del symbol_samples[:7 + n_derivative_contracts]
    #         except IndexError:
    #             break
    #
    #     ui.update_switch(id='show_matching_stocks', value=stocks.shape[0] > 0)
    #
    #     matching_symbols.set({'stocks': stocks, 'bonds': bonds})
    #
    # @render.data_frame
    # def matching_stock_symbols_df():
    #     return render.DataTable(matching_symbols()['stocks'])
    #
    # @render.data_frame
    # def matching_bond_symbols_df():
    #     return render.DataTable(matching_symbols()['bonds'])
    #
    # # Contract Details #########################################################
    #
    # contract_details = reactive.value()
    #
    # @reactive.effect
    # def update_cd_contract_definition():
    #     ui.update_text_area(
    #         id='cd_contract_definition',
    #         value=input.cd_example_contract()
    #     )
    #
    # @reactive.effect
    # @reactive.event(
    #     input.cd_request_contract_details_btn,
    #     ignore_init=True
    # )
    # def request_contract_details():
    #
    #     try:
    #         exec(input.cd_contract_definition())
    #     except Exception as e:
    #         print(e)
    #         return
    #
    #     rcd_contract = None
    #     for key, value in locals().items():
    #         if isinstance(value, Contract):
    #             rcd_contract = value
    #
    #     if rcd_contract is None:
    #         ui.notification_show('No viable contract object found')
    #         return
    #
    #     (rd, wt, er) = select.select([], [ib_socket], [])
    #     wt[0].send(
    #         rxt.req_contract_details(
    #             reqId=next_valid_id(),
    #             contract=rcd_contract
    #         )
    #     )
    #
    # @reactive.effect
    # @reactive.event(input.contract_details)
    # def update_contract_details():
    #
    #     cdeets = input.contract_details()
    #
    #     contract_details_lst = []
    #
    #     for i in range(len(cdeets)):
    #         match cdeets[i][1]:
    #             case 'OPT':
    #                 match len(cdeets[i]):
    #                     case 34:
    #                         contract_details_lst.append(
    #                             pd.DataFrame({
    #                                 'symbol': [cdeets[i][0]],
    #                                 'secType': [cdeets[i][1]],
    #                                 'lastTradeDate': [cdeets[i][2]],
    #                                 'strike': [cdeets[i][3]],
    #                                 'right': [cdeets[i][4]],
    #                                 'exchange': [cdeets[i][5]],
    #                                 'currency': [cdeets[i][6]],
    #                                 'localSymbol': [cdeets[i][7]],
    #                                 'marketName': [cdeets[i][8]],
    #                                 'tradingClass': [cdeets[i][9]],
    #                                 'conId': [cdeets[i][10]],
    #                                 'minTick': [cdeets[i][11]],
    #                                 'multiplier': [cdeets[i][12]],
    #                                 'orderTypes': [cdeets[i][13]],
    #                                 'validExchanges': [cdeets[i][14]],
    #                                 'priceMagnifier': [cdeets[i][15]],
    #                                 'underConID': [cdeets[i][16]],
    #                                 'longName': [cdeets[i][17]],
    #                                 'contractMonth': [cdeets[i][18]],
    #                                 'industry': [cdeets[i][19]],
    #                                 'category': [cdeets[i][20]],
    #                                 'subcategory': [cdeets[i][21]],
    #                                 'timeZoneId': [cdeets[i][22]],
    #                                 'tradingHours': [cdeets[i][23]],
    #                                 'liquidHours': [cdeets[i][24]],
    #                                 'aggGroup': [cdeets[i][26]],
    #                                 'underSymbol': [cdeets[i][27]],
    #                                 'underSecType': [cdeets[i][28]],
    #                                 'marketRuleIds': [cdeets[i][29]],
    #                                 'realExpirationDate': [cdeets[i][30]],
    #                                 'minSize': [cdeets[i][31]],
    #                                 'sizeIncrement': [cdeets[i][32]],
    #                                 'suggestedSizeIncrement': [cdeets[i][33]]
    #                             })
    #                         )
    #                     case 31:
    #                         contract_details_lst.append(
    #                             pd.DataFrame({
    #                                 'symbol': [cdeets[i][0]],
    #                                 'secType': [cdeets[i][1]],
    #                                 'lastTradeDate': [cdeets[i][2]],
    #                                 'strike': [cdeets[i][3]],
    #                                 'right': [cdeets[i][4]],
    #                                 'exchange': [cdeets[i][5]],
    #                                 'currency': [cdeets[i][6]],
    #                                 'localSymbol': [cdeets[i][7]],
    #                                 'marketName': [cdeets[i][8]],
    #                                 'tradingClass': [cdeets[i][9]],
    #                                 'conId': [cdeets[i][10]],
    #                                 'minTick': [cdeets[i][11]],
    #                                 'multiplier': [cdeets[i][12]],
    #                                 'orderTypes': [cdeets[i][13]],
    #                                 'validExchanges': [cdeets[i][14]],
    #                                 'priceMagnifier': [cdeets[i][15]],
    #                                 'underConID': [cdeets[i][16]],
    #                                 'longName': [cdeets[i][17]],
    #                                 'contractMonth': [cdeets[i][18]],
    #                                 'industry': [cdeets[i][19]],
    #                                 'category': [cdeets[i][20]],
    #                                 'subcategory': [cdeets[i][21]],
    #                                 'aggGroup': [cdeets[i][23]],
    #                                 'underSymbol': [cdeets[i][24]],
    #                                 'underSecType': [cdeets[i][25]],
    #                                 'marketRuleIds': [cdeets[i][26]],
    #                                 'realExpirationDate': [cdeets[i][27]],
    #                                 'minSize': [cdeets[i][28]],
    #                                 'sizeIncrement': [cdeets[i][29]],
    #                                 'suggestedSizeIncrement': [cdeets[i][30]]
    #                             })
    #                         )
    #                     case _:
    #                         contract_details_lst.append(
    #                             pd.DataFrame({
    #                                 'symbol': [cdeets[i][0]],
    #                                 'secType': [cdeets[i][1]],
    #                                 'lastTradeDate': [cdeets[i][2]],
    #                                 'strike': [cdeets[i][3]],
    #                                 'right': [cdeets[i][4]],
    #                                 'exchange': [cdeets[i][5]],
    #                                 'currency': [cdeets[i][6]],
    #                                 'localSymbol': [cdeets[i][7]],
    #                                 'marketName': [cdeets[i][8]],
    #                                 'tradingClass': [cdeets[i][9]],
    #                                 'conId': [cdeets[i][10]],
    #                                 'minTick': [cdeets[i][11]],
    #                                 'multiplier': [cdeets[i][12]],
    #                                 'orderTypes': [cdeets[i][13]],
    #                                 'validExchanges': [cdeets[i][14]],
    #                                 'priceMagnifier': [cdeets[i][15]],
    #                                 'underConID': [cdeets[i][16]],
    #                                 'longName': [cdeets[i][17]],
    #                                 'contractMonth': [cdeets[i][18]],
    #                                 'aggGroup': [cdeets[i][20]],
    #                                 'underSymbol': [cdeets[i][21]],
    #                                 'underSecType': [cdeets[i][22]],
    #                                 'marketRuleIds': [cdeets[i][23]],
    #                                 'realExpirationDate': [cdeets[i][24]],
    #                                 'minSize': [cdeets[i][25]],
    #                                 'sizeIncrement': [cdeets[i][26]],
    #                                 'suggestedSizeIncrement': [cdeets[i][27]]
    #                             })
    #                         )
    #             case 'STK':
    #                 # 'STK' is the default case
    #                 end_of_sec_id_list_ind = 23 + 2 * int(cdeets[i][22])
    #                 contract_details_lst.append(
    #                     pd.DataFrame({
    #                         'symbol': [cdeets[i][0]],
    #                         'secType': [cdeets[i][1]],
    #                         'exchange': [cdeets[i][3]],
    #                         'currency': [cdeets[i][4]],
    #                         'localSymbol': [cdeets[i][5]],
    #                         'marketName': [cdeets[i][6]],
    #                         'tradingClass': [cdeets[i][7]],
    #                         'conId': [cdeets[i][8]],
    #                         'minTick': [cdeets[i][9]],
    #                         'orderTypes': [cdeets[i][10]],
    #                         'validExchanges': [cdeets[i][11]],
    #                         'priceMagnifier': [cdeets[i][12]],
    #                         'underConID': [cdeets[i][13]],
    #                         'longName': [cdeets[i][14]],
    #                         'primaryExchange': [cdeets[i][15]],
    #                         'industry': [cdeets[i][16]],
    #                         'category': [cdeets[i][17]],
    #                         'subcategory': [cdeets[i][18]],
    #                         'timeZoneId': [cdeets[i][19]],
    #                         'tradingHours': [cdeets[i][20]],
    #                         'liquidHours': [cdeets[i][21]],
    #                         'secIdList': ["{" + ",".join([
    #                             "'" + "':'".join(cdeets[i][x:(x + 2)]) + "'" for
    #                             x in range(23, end_of_sec_id_list_ind, 2)
    #                         ]) + "}"],
    #                         'aggGroup': [cdeets[i][end_of_sec_id_list_ind]],
    #                         'marketRuleIds': [
    #                             cdeets[i][end_of_sec_id_list_ind + 1]
    #                         ],
    #                         'stockType': [
    #                             cdeets[i][end_of_sec_id_list_ind + 2]],
    #                         'minSize': [cdeets[i][end_of_sec_id_list_ind + 3]],
    #                         'sizeIncrement': [
    #                             cdeets[i][end_of_sec_id_list_ind + 4]
    #                         ],
    #                         'suggestedSizeIncrement': [
    #                             cdeets[i][end_of_sec_id_list_ind + 5]
    #                         ]
    #                     })
    #                 )
    #             case _:
    #                 pd.DataFrame({cdeets})
    #
    #     contract_details.set(pd.concat(contract_details_lst, ignore_index=True))
    #
    # @render.data_frame
    # def contract_details_df():
    #     return render.DataTable(contract_details())
    #
    # # Security-Defined Option Parameters #######################################
    #
    # sec_def_opt_params = reactive.value()
    #
    # @reactive.effect
    # @reactive.event(
    #     input.req_sec_def_opt_params_btn,
    #     ignore_init=True
    # )
    # def request_sec_def_opt_params():
    #     (rd, wt, er) = select.select([], [ib_socket], [])
    #     wt[0].send(
    #         rxt.req_sec_def_opt_params(
    #             reqId=next_valid_id(),
    #             underlyingSymbol=input.sdop_underlying_symbol(),
    #             futFopExchange=input.sdop_fut_fop_exchange(),
    #             underlyingSecType=input.sdop_underlying_sec_type(),
    #             underlyingConId=input.sdop_underlying_con_id()
    #         )
    #     )
    #
    # @reactive.effect
    # @reactive.event(input.sec_def_opt_params)
    # def update_sec_def_opt_params():
    #     sdop_lst = list(input.sec_def_opt_params())
    #     sec_def_opt_params_lst = []
    #
    #     for i in range(len(sdop_lst)):
    #         n_expiries = int(sdop_lst[i][4])
    #         sec_def_opt_params_lst.append(
    #             pd.DataFrame({
    #                 'exchange': [sdop_lst[i][0]],
    #                 'underlying_con_id': [sdop_lst[i][1]],
    #                 'trading_class': [sdop_lst[i][2]],
    #                 'multiplier': [sdop_lst[i][3]],
    #                 'expirations': ",".join(sdop_lst[i][5:5+n_expiries]),
    #                 'strikes': ",".join(
    #                     sdop_lst[i][5+n_expiries:len(sdop_lst[i])]
    #                 )
    #             })
    #         )
    #
    #     sec_def_opt_params.set(
    #         pd.concat(sec_def_opt_params_lst, ignore_index=True)
    #         .sort_values('exchange')
    #     )
    #
    # @render.data_frame
    # def sec_def_opt_params_df():
    #     return render.DataTable(sec_def_opt_params())
    #
    # # Market Data ##############################################################
    #
    # mkt_data = reactive.value({})
    #
    # @reactive.effect
    # def update_md_contract_definition():
    #     ui.update_text_area(
    #         id='md_contract_definition',
    #         value=input.md_example_contract() +
    #               "\n" +
    #               "genericTickList=''\n" +
    #               "snapshot=0\n" +
    #               "regulatorySnapshot=0\n" +
    #               "mktDataOptions=''"
    #     )
    #
    # @reactive.effect
    # @reactive.event(
    #     input.md_request_market_data_btn,
    #     ignore_init=True
    # )
    # def request_market_data():
    #     mkt_dta = mkt_data()
    #     exec(input.md_contract_definition())
    #     # creates the following local variables from the user's input:
    #     #   contract: a contract object
    #     #   genericTickList: '' by default
    #     #   snapshot: 0 by default
    #     #   regulatorySnapshot: 0 by default
    #     #   mktDataOptions: '' by default
    #     (rd, wt, er) = select.select([], [ib_socket], [])
    #     nxt_valid_id = next_valid_id()
    #     wt[0].send(
    #         eval(
    #             "rxt.req_mkt_data(" + str(nxt_valid_id) + ", contract, " +
    #             "genericTickList, snapshot, regulatorySnapshot, mktDataOptions)"
    #         )
    #     )
    #     mkt_dta.update({
    #         nxt_valid_id: {
    #             key: value for (key, value) in
    #             eval('contract.__dict__.items()') if
    #             value is not None and value != 0 and value != ''
    #         }
    #     })
    #     mkt_data.set(mkt_dta.copy())
    #
    # @reactive.effect
    # @reactive.event(input.tick_req_params)
    # def update_tick_req_params():
    #     mkt_dta = mkt_data()
    #     trp = input.tick_req_params()
    #     t_r_p = {
    #         'minTick': trp[1],
    #         'bboExchange': trp[2]
    #     }
    #     try:
    #         t_r_p['snapshotPermissions'] = trp[3]
    #     except IndexError:
    #         pass
    #     mkt_dta[trp[0]].update(t_r_p)
    #     mkt_data.set(mkt_dta.copy())
    #
    # @reactive.effect
    # @reactive.event(input.tick_price)
    # def update_tick_price():
    #     mkt_dta = mkt_data()
    #     tp = input.tick_price()
    #     mkt_dta[tp[1]].update({
    #         TickTypeEnum.to_str(int(tp[2])): float(tp[3])
    #     })
    #     mkt_data.set(mkt_dta.copy())
    #
    # @reactive.effect
    # @reactive.event(input.tick_size)
    # def update_tick_size():
    #     mkt_dta = mkt_data()
    #     tp = input.tick_size()
    #     mkt_dta[tp[1]].update({TickTypeEnum.to_str(int(tp[2])): float(tp[3])})
    #     mkt_data.set(mkt_dta.copy())
    #
    # @reactive.effect
    # @reactive.event(input.tick_generic)
    # def update_tick_generic():
    #     mkt_dta = mkt_data()
    #     tp = input.tick_generic()
    #     mkt_dta[tp[1]].update({TickTypeEnum.to_str(int(tp[2])): float(tp[3])})
    #     mkt_data.set(mkt_dta.copy())
    #
    # @reactive.effect
    # @reactive.event(input.tick_string)
    # def update_tick_generic():
    #     mkt_dta = mkt_data()
    #     tp = input.tick_string()
    #     mkt_dta[tp[1]].update({TickTypeEnum.to_str(int(tp[2])): tp[3]})
    #     mkt_data.set(mkt_dta.copy())
    #
    # @render.text
    # def mkt_data_txt():
    #     temp_out = StringIO()
    #     sys.stdout = temp_out
    #     print(mkt_data())
    #     sys.stdout = sys.__stdout__
    #     return temp_out.getvalue()
    #
    # # """Script""" #############################################################
    #
    # @reactive.effect
    # @reactive.event(input.flying_bar_start_btn, ignore_init=True)
    # def begin_flying_bars():
    #     (rd, wt, er) = select.select([], [ib_socket], [])
    #     wt[0].send(
    #         rxt.req_sec_def_opt_params(
    #             reqId=next_valid_id(),
    #             underlyingSymbol=input.flying_bar_underlying_symbol(),
    #             futFopExchange="",
    #             underlyingSecType=input.flying_bar_underlying_sec_type(),
    #             underlyingConId=input.flying_bar_underlying_con_id()
    #         )
    #     )
    #     next_valid_id.set(str(int(next_valid_id()) + 1))
    #
    #     contract = Contract()
    #     contract.symbol = input.flying_bar_underlying_symbol()
    #     contract.secType = input.flying_bar_underlying_sec_type()
    #     contract.currency = "USD"
    #     contract.exchange = "SMART"
    #
    #     genericTickList = ''
    #     snapshot = 0
    #     regulatorySnapshot = 0
    #     mktDataOptions = ''
    #
    #     mkt_dta = mkt_data()
    #
    #     (rd, wt, er) = select.select([], [ib_socket], [])
    #     nxt_valid_id = next_valid_id()
    #     wt[0].send(
    #         eval(
    #             "rxt.req_mkt_data(" + str(nxt_valid_id) + ", contract, " +
    #             "genericTickList, snapshot, regulatorySnapshot, mktDataOptions)"
    #         )
    #     )
    #     mkt_dta.update({
    #         nxt_valid_id: {
    #             key: value for (key, value) in
    #             eval('contract.__dict__.items()') if
    #             value is not None and value != 0 and value != ''
    #         }
    #     })
    #     mkt_data.set(mkt_dta.copy())