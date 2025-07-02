import datetime, select, threading, os, re

import numpy as np
import pandas as pd
import requests

from shinybroker import VERSION
from shinybroker.connection import (
    create_ibkr_socket_conn,
    ib_msg_reader_run_loop
)
from shinybroker.obj_defs import *
from shinybroker.msgs_to_ibkr import *
from shinybroker.format_ibkr_inputs import format_contract_details
from shinybroker.functionary import functionary
from shiny import Inputs, Outputs, Session, reactive, render, ui
from sys import exit


def sb_server(
        input: Inputs, output: Outputs, session: Session,
        host, port, client_id, verbose
):

    def version_to_int_list(version_str):
        return list(map(int, version_str.split(".")))

    latest_version = requests.get(
            "https://pypi.org/pypi/shinybroker/json",
            timeout=5
        ).json()['info']['version']

    if any(
            [remote > local for remote, local in zip(
                version_to_int_list(latest_version),
                version_to_int_list(VERSION)
            )]
    ):
        ui.modal_show(
            ui.modal(
                ui.HTML(
                    "You are using ShinyBroker Version <strong>" +
                    VERSION +
                    "</strong> but Version <strong>" +
                    latest_version +
                    "</strong> is available.<br><br>"
                    "Because ShinyBroker is under frequent development, it "
                    "is highly recommended that you update to the latest "
                    "version. To do so, please: <ol>"
                    "<li>Stop your ShinyBroker app</li>"
                    "<li>Run <code>pip install shinybroker --upgrade</code> " 
                    "in your terminal</li> "
                    "<li> Restart your ShinyBroker app</li>"
                    "</ol> Doing so will ensure that you have access to the "
                    "latest features and bug fixes."
                ),
                title="Please Update ShinyBroker",
                easy_close=True
            )
        )

    # host='127.0.0.1'
    # port=7497
    # client_id=10742

    try:
        ib_conn = create_ibkr_socket_conn(
            host=host, port=port, client_id=client_id
        )
    except ConnectionRefusedError:
        ui.modal_show(
            ui.modal(
                ui.HTML(
                    "ShinyBroker tried to connect to an IBKR client on <br>"
                    "<br><strong>host</strong>: " + str(host) + "<br>" +
                    "<strong>port</strong>: " + str(port) + "<br>" +
                    "<strong>client_id</strong>: " + str(client_id) + "<br>" +
                    "<br>...but connection was refused. Please make sure that "
                    "an IBKR client such as TWS or IBKG is running and "
                    "configured to accept API connections. See the <a href = "
                    "'https://shinybroker.com'>ShinyBroker website</a> for "
                    "a detailed setup example."
                ),
                title="Can't connect to IBKR",
                easy_close=True
            )
        )
        exit(0)
        return None

    ib_socket = ib_conn['ib_socket']
    session.on_ended(ib_socket.close)


    print(
        'Connected to IBKR at ' + ib_conn['CONNECTION_TIME'] +
        ' under API protocol version ' + ib_conn['API_VERSION']
    )
    print(
        'host: ' + host + "\nport: " + str(port) +
        "\nclient_id: " + str(client_id)
    )

    connection_info = reactive.value(
        pd.DataFrame({
            'connection_time': [ib_conn['CONNECTION_TIME']],
            'api_version': [ib_conn['API_VERSION']]
        })
    )

    # Creates a thread object for the async function that reads incoming
    #   messages from the socket
    # Passes to that function:
    #   - the socket connection
    #   - the Shiny session
    # Starts the thread
    ib_msg_reader_thread = threading.Thread(
        target=ib_msg_reader_run_loop,
        kwargs={
            'ib_sock': ib_socket,
            'shiny_sesh': session,
            'verbose': verbose
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

    @render.text
    def market_data_type_txt():

        match market_data_type():
            case "1":
                mdt = "1: Live"
            case "2":
                mdt = "2: Frozen"
            case "3":
                mdt = "3: Delayed"
            case "4":
                mdt = "4: Delayed Frozen"
            case _:
                mdt = market_data_type()

        return "Received Mkt Data Type " + mdt

    # Managed Accounts

    managed_accounts = reactive.value([])

    @reactive.effect
    @reactive.event(input.managed_accounts)
    def update_managed_accounts():
        managed_accounts.set(list(input.managed_accounts())[1:])

    # Next Valid ID

    next_valid_id = reactive.value(ib_conn['NEXT_VALID_ID'])

    @reactive.effect
    @reactive.event(input.next_valid_id)
    def update_next_valid_id():
        next_valid_id.set(input.next_valid_id()[1])

    @render.text
    def next_valid_id_txt():
        return "Next Valid ID: " + str(next_valid_id())

    # Error Messages

    error_messages = reactive.value(
        pd.DataFrame(
            columns=["error_id", "error_code", "error_message"],
            index=None
        )
    )

    @reactive.effect
    @reactive.event(input.error_message)
    def update_error_messages():
        err_msgs = error_messages()
        new_msg = input.error_message()
        error_messages.set(
            pd.concat(
                [
                    err_msgs,
                    pd.DataFrame(
                        {
                            "error_id": new_msg[1],
                            "error_code": new_msg[2],
                            "error_message": new_msg[3]
                        },
                        index=[len(err_msgs)]
                    )
                ],
                axis=0
            )
        )

    @render.table
    def error_messages_df():
        return error_messages().style.set_table_attributes(
            'class="dataframe shiny-table table w-auto"'
        ).hide(axis="index")

    @reactive.effect
    @reactive.event(input.error_notification)
    def send_error_message_notification():
        ui.notification_show(input.error_notification(), duration=30)

    # Current Time
    # Useful mostly just to check if i/o is working.
    # Runs when the user clicks the req_current_time button and updates the

    current_time = reactive.value()

    @reactive.effect
    @reactive.event(input.req_current_time, ignore_init=True)
    def request_current_time():
        (rd, wt, er) = select.select([], [ib_socket], [])
        wt[0].send(req_current_time())

    @reactive.effect
    @reactive.event(input.current_time)
    def update_current_time():
        current_time.set(
            str(datetime.datetime.fromtimestamp(int(input.current_time()[1])))
        )

    @render.text
    def current_time_txt():
        return current_time()

    # Matching Symbols #########################################################

    matching_symbols = reactive.value()

    @reactive.effect
    @reactive.event(input.req_matching_symbols)
    def request_matching_symbols():
        (rd, wt, er) = select.select([], [ib_socket], [])
        wt[0].send(
            req_matching_symbols(
                reqId=next_valid_id(),
                pattern=input.requested_symbol()
            )
        )

    @reactive.effect
    @reactive.event(input.symbol_samples)
    def update_matching_symbols():

        symbol_samples = list(input.symbol_samples())[2:]

        bonds = []

        while True:
            try:
                bond_ind = symbol_samples.index('-1')
                bonds.append(
                    pd.DataFrame.from_dict({
                        'issuer': [symbol_samples[bond_ind + 3]],
                        'issuer_id': [symbol_samples[bond_ind + 4]]
                    })
                )
                del symbol_samples[bond_ind:bond_ind + 5]
            except ValueError:
                break

        ui.update_switch(id='show_matching_bonds', value=len(bonds) > 0)

        stocks = []

        while True:
            try:
                n_derivative_contracts = int(symbol_samples[5])
                stocks.append(
                    pd.DataFrame.from_dict({
                        'con_id': [symbol_samples[0]],
                        'symbol': [symbol_samples[1]],
                        'sec_type': [symbol_samples[2]],
                        'primary_exchange': [symbol_samples[3]],
                        'currency': [symbol_samples[4]],
                        'derivative_sec_types': ",".join(
                            symbol_samples[6:5 + n_derivative_contracts]
                        ),
                        'description': [
                            symbol_samples[6 + n_derivative_contracts]]
                    })
                )
                del symbol_samples[:7 + n_derivative_contracts]
            except IndexError:
                break

        ui.update_switch(id='show_matching_stocks', value=len(stocks) > 0)

        if not bonds:
            if not stocks:
                ui.notification_show('No matching symbols found')
            else:
                matching_symbols.set({
                    'stocks': pd.concat(stocks, ignore_index=True)
                })
        else:
            if not stocks:
                matching_symbols.set({
                    'bonds': pd.concat(bonds, ignore_index=True)
                })
            else:
                matching_symbols.set({
                    'stocks': pd.concat(stocks, ignore_index=True),
                    'bonds': pd.concat(bonds, ignore_index=True)
                })

    @render.data_frame
    def matching_stock_symbols_df():
        return render.DataTable(matching_symbols()['stocks'])

    @render.data_frame
    def matching_bond_symbols_df():
        return render.DataTable(matching_symbols()['bonds'])

    # Contract Details #########################################################

    contract_details = reactive.value()

    @reactive.effect
    def update_cd_contract_definition():
        ui.update_text_area(
            id='cd_contract_definition',
            value=input.cd_example_contract()
        )

    @reactive.effect
    @reactive.event(
        input.cd_request_contract_details_btn,
        ignore_init=True
    )
    def request_contract_details():

        try:
            namespace = {}
            exec('from shinybroker import Contract', namespace)
            exec(input.cd_contract_definition(), namespace)
        except Exception as e:
            print(e)
            return

        rcd_contract = None
        for key, value in namespace.items():
            if isinstance(value, Contract):
                rcd_contract = value
                break

        if rcd_contract is None:
            ui.notification_show('No viable contract object found')
            return

        (rd, wt, er) = select.select([], [ib_socket], [])
        wt[0].send(
            req_contract_details(
                reqId=next_valid_id(),
                contract=rcd_contract
            )
        )

    @reactive.effect
    @reactive.event(input.contract_details)
    def update_contract_details():
        cdeets = input.contract_details()
        cdeets_df = format_contract_details(cdeets)
        contract_details.set(cdeets_df)

    @render.data_frame
    def contract_details_df():
        return render.DataTable(contract_details())

    # Security-Defined Option Parameters #######################################

    sec_def_opt_params = reactive.value()

    @reactive.effect
    @reactive.event(
        input.req_sec_def_opt_params_btn,
        ignore_init=True
    )
    def request_sec_def_opt_params():
        (rd, wt, er) = select.select([], [ib_socket], [])
        wt[0].send(
            req_sec_def_opt_params(
                reqId=next_valid_id(),
                underlyingSymbol=input.sdop_underlying_symbol(),
                futFopExchange=input.sdop_fut_fop_exchange(),
                underlyingSecType=input.sdop_underlying_sec_type(),
                underlyingConId=input.sdop_underlying_con_id()
            )
        )

    @reactive.effect
    @reactive.event(input.sec_def_opt_params)
    def update_sec_def_opt_params():
        sdop_lst = list(input.sec_def_opt_params())
        sec_def_opt_params_lst = []

        for i in range(len(sdop_lst)):
            n_expiries = int(sdop_lst[i][4])
            sec_def_opt_params_lst.append(
                pd.DataFrame({
                    'exchange': [sdop_lst[i][0]],
                    'underlying_con_id': [sdop_lst[i][1]],
                    'trading_class': [sdop_lst[i][2]],
                    'multiplier': [sdop_lst[i][3]],
                    'expirations': ",".join(sdop_lst[i][5:5+n_expiries]),
                    'strikes': ",".join(
                        sdop_lst[i][6+n_expiries:len(sdop_lst[i])]
                    )
                })
            )

        sec_def_opt_params.set(
            pd.concat(sec_def_opt_params_lst, ignore_index=True)
            .sort_values('exchange')
        )

    @render.data_frame
    def sec_def_opt_params_df():
        return render.DataTable(sec_def_opt_params())

    # Market Data ##############################################################

    mkt_data = reactive.value({})

    @reactive.effect
    def update_md_contract_definition():
        ui.update_text_area(
            id='md_contract_definition',
            value=input.md_example_contract()
        )

    @reactive.effect
    @reactive.event(
        input.md_request_market_data_btn,
        ignore_init=True
    )
    def request_market_data():
        mkt_dta = mkt_data()
        exec(input.md_contract_definition())
        (rd, wt, er) = select.select([], [ib_socket], [])
        try:
            subscription_id = max(list(map(int, mkt_dta.keys()))) + 1
        except ValueError:
            subscription_id = 1
        subscription_id = str(subscription_id)
        wt[0].send(
            eval(
                "req_mkt_data(" + subscription_id + ", contract, " +
                "genericTickList, snapshot, regulatorySnapshot)"
            )
        )
        mkt_dta.update({subscription_id: eval('contract.compact()')})
        mkt_data.set(mkt_dta.copy())

    @reactive.effect
    @reactive.event(input.tick_req_params)
    def update_tick_req_params():
        mkt_dta = mkt_data()
        trp = input.tick_req_params()
        t_r_p = {
            'minTick': trp[1],
            'bboExchange': trp[2]
        }
        try:
            t_r_p['snapshotPermissions'] = trp[3]
        except IndexError:
            pass
        mkt_dta[trp[0]].update(t_r_p)
        mkt_data.set(mkt_dta.copy())

    @reactive.effect
    @reactive.event(input.tick_price)
    def update_tick_price():
        mkt_dta = mkt_data()
        tp = input.tick_price()
        mkt_dta[tp[1]].update({
            functionary['tick_type'][int(tp[2])]: float(tp[3])
        })
        mkt_data.set(mkt_dta.copy())

    @reactive.effect
    @reactive.event(input.tick_size)
    def update_tick_size():
        mkt_dta = mkt_data()
        tp = input.tick_size()
        mkt_dta[tp[1]].update(
            {functionary['tick_type'][int(tp[2])]: float(tp[3])}
        )
        mkt_data.set(mkt_dta.copy())

    @reactive.effect
    @reactive.event(input.tick_generic)
    def update_tick_generic():
        mkt_dta = mkt_data()
        tp = input.tick_generic()
        mkt_dta[tp[1]].update(
            {functionary['tick_type'][int(tp[2])]: float(tp[3])}
        )
        mkt_data.set(mkt_dta.copy())

    @reactive.effect
    @reactive.event(input.tick_string)
    def update_tick_generic():
        mkt_dta = mkt_data()
        tp = input.tick_string()
        mkt_dta[tp[1]].update(
            {functionary['tick_type'][int(tp[2])]: tp[3]}
        )
        mkt_data.set(mkt_dta.copy())

    @render.text
    def mkt_data_txt():
        return re.sub("},", "},\n\t", str(mkt_data().__repr__()))

    # Historical Data ##########################################################

    historical_data = reactive.value({})

    @reactive.effect
    def update_hd_contract_definition():
        ui.update_text_area(
            id='hd_contract_definition',
            value=input.hd_example_contract()
        )

    @reactive.effect
    @reactive.event(
        input.hd_request_market_data_btn,
        ignore_init=True
    )
    def request_historical_data():
        hd = historical_data()
        exec(input.hd_contract_definition())
        (rd, wt, er) = select.select([], [ib_socket], [])
        try:
            subscription_id = max(list(map(int, hd.keys()))) + 1
        except ValueError:
            subscription_id = 1
        subscription_id = str(subscription_id)
        wt[0].send(
            eval(
                "req_historical_data(" + subscription_id + ", contract, " +
                "endDateTime, durationStr, barSizeSetting, whatToShow, " +
                "useRTH, formatDate, keepUpToDate)"
            )
        )
        hd.update({subscription_id: eval('contract.compact()')})
        historical_data.set(hd.copy())

    @reactive.effect
    @reactive.event(input.historical_data)
    def add_new_historical_data():
        hd = historical_data()
        hst_dta = input.historical_data()
        hd_len = len(hst_dta)
        hd[hst_dta[0]].update({
            'startDateStr': hst_dta[1],
            'endDateStr': hst_dta[2],
            'hst_dta': pd.DataFrame({
                'timestamp': [hst_dta[i] for i in range(4, hd_len, 8)],
                'open': [float(hst_dta[i]) for i in range(5, hd_len, 8)],
                'high': [float(hst_dta[i]) for i in range(6, hd_len, 8)],
                'low': [float(hst_dta[i]) for i in range(7, hd_len, 8)],
                'close': [float(hst_dta[i]) for i in range(8, hd_len, 8)],
                'volume': [int(hst_dta[i]) for i in range(9, hd_len, 8)],
                'wap': [
                    round(float(hst_dta[i]), 3) for i in range(10, hd_len, 8)
                ],
                'barCount': [int(hst_dta[i]) for i in range(11, hd_len, 8)]
                # np.array(hst_dta[4:]).reshape(int(hst_dta[3]), 8),
                # columns=['date', 'open', 'high', 'low', 'close', 'volume',
                #          'wap', 'barCount']
            })
        })
        historical_data.set(hd.copy())

    @reactive.effect
    @reactive.event(input.historical_data_update)
    def update_historical_data():
        hd = historical_data()
        hdu = list(input.historical_data_update())
        hdu[7] = round(float(hdu[7]), 3)
        try:
            hd[hdu[0]]['hst_dta'].loc[
            np.where(hd[hdu[0]]['hst_dta']['timestamp'] == hdu[2])[0][0], :
            ] = [hdu[i] for i in [2, 3, 5, 6, 4, 8, 7, 1]]
        except IndexError:
            hd[hdu[0]]['hst_dta'] = pd.concat(
                [
                    hd[hdu[0]]['hst_dta'],
                    pd.DataFrame(
                        hdu[1:],
                        index=['barCount', 'timestamp', 'open', 'close', 'high',
                               'low', 'wap', 'volume']
                    ).transpose()
                ],
                axis=0,
                ignore_index=True
            )
        historical_data.set(hd.copy())

    @render.text
    def historical_data_txt():
        return re.sub(
            pattern="},",
            repl="},\n\t",
            string=str(historical_data().__repr__())
        )

    sb_rvs = dict({
        'connection_info': connection_info,
        'contract_details': contract_details,
        'current_time': current_time,
        'error_messages': error_messages,
        'historical_data': historical_data,
        'managed_accounts': managed_accounts,
        'market_data_type': market_data_type,
        'matching_symbols': matching_symbols,
        'mkt_data': mkt_data,
        'next_valid_id': next_valid_id,
        'sec_def_opt_params': sec_def_opt_params
    })

    return ib_socket, sb_rvs
