import pandas as pd
import warnings

from datetime import datetime
from shinybroker.connection import (
    create_ibkr_socket_conn, send_ib_message, read_ib_msg
)
from shinybroker.format_ibkr_inputs import (
    format_historical_data_input,
    format_sec_def_opt_params_input,
    format_symbol_samples_input
)
from shinybroker.functionary import functionary
from shinybroker.msgs_to_ibkr import (
    req_historical_data,
    req_matching_symbols,
    req_sec_def_opt_params
)
from shinybroker.obj_defs import Contract


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
    """Fetch the option parameters for a security.

    Creates a temporary IBKR client socket at the specified `host`, `port`, and
    `client_id`, then makes a query for the security-defined option parameters
    for the security defined by `underlyingConId`, `underlyingSymbol`,
    `underlyingSecType`, and `futFopExchange`.

    `fetch_sec_def_opt_params` will collect all
    `SECURITY_DEFINITION_OPTION_PARAMETER` messages it receives and return
    them in a dataframe when it receives a
    `SECURITY_DEFINITION_OPTION_PARAMETER_END` message.

    If `timeout` number of seconds elapse before receiving
    `SECURITY_DEFINITION_OPTION_PARAMETER_END`, then `fetch_sec_def_opt_params`
    returns `None`.

    Upon completion, `fetch_sec_def_opt_params` closes the socket it opened.

    Parameters
    ------------
    underlyingConId: int
        `conId` of the underlying security
    underlyingSymbol: str
        Symbol of the underlying security for which you want option parameters.
    underlyingSecType: str
        Type of the underlying security; e.g., "`STK`"
    host: '127.0.0.1'
        Address of a running IBKR client (such as TWS or IBG) that has been
        configured to accept API connections
    port: 7497
        Port of a running IBKR client
    client_id: 9999
        Client ID you want to use for the request. If you are connecting to a
        system that is used by multiple users, then you may wish to set aside an
         ID for this purpose; if you're the only one using the account then
         you probably don't have to worry about it -- just use the default.
    futFopExchange: ""
        Only set this parameter if the underlying is a futures contract; in
        other words, don't change it from the default `""` if your underlying is
         a stock. If your underlying **is** a futures contract, then use
         `futFopExchange` to specify the exchange for which you want option
         parameters. You may still pass in `""` if you want the results to
         include **all** of the exchanges available at IBKR that trade
         options on your specified underlying.
    timeout: 3
        Time in seconds to wait for a response.

    Examples
    --------
    ```
    {{< include ../examples/fetch_sec_def_opt_params.py >}}
    ```
    """
    ib_conn = create_ibkr_socket_conn(
        host=host, port=port, client_id=client_id
    )
    ib_socket = ib_conn['ib_socket']
    ib_socket.settimeout(1)

    incoming_msg = read_ib_msg(ib_socket)

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

    sdops = []
    start_time = datetime.now()
    while incoming_msg[0] != functionary['incoming_msg_codes'][
        'SECURITY_DEFINITION_OPTION_PARAMETER_END'
    ]:
        incoming_msg = read_ib_msg(sock=ib_socket)
        if incoming_msg[0] == functionary['incoming_msg_codes'][
            'SECURITY_DEFINITION_OPTION_PARAMETER'
        ]:
            sdops.append(
                format_sec_def_opt_params_input(sdop=incoming_msg[2:]))
        if (datetime.now() - start_time).seconds > timeout:
            break

    try:
        sec_def_opt_params = pd.concat(
            sdops,
            ignore_index=True
        ).sort_values('exchange')
    except ValueError:
        sec_def_opt_params = None

    ib_socket.close()

    return sec_def_opt_params


def fetch_historical_data(
        contract: Contract,
        endDateTime="",
        durationStr="1 D",
        barSizeSetting='1 hour',
        whatToShow='Trades',
        useRTH=True,
        host='127.0.0.1',
        port=7497,
        client_id=9999,
        timeout=3
):
    """Fetch historical data for a tradable asset

    Creates a temporary IBKR client socket at the specified `host`, `port`, and
    `client_id`, then makes a query for the historical data specified by the
    input parameters, receives the response, closes the socket, formats the
    response, and returns the result.

    If `timeout` number of seconds elapse before receiving historical data,
    then `fetch_historical_data` returns `None`.

    Parameters
    ------------
    contract: Contract
        The [Contract](`shinybroker.Contract`) object for which you want data
    endDateTime: ""
        Ending datetime string formatted as “YYYYMMDD HH:mm:ss TMZ”
        specifying the end of the time period for which you want historical
        data. Leave it as the default "" to get historical data up to the
        current present moment.
    durationStr: "1 D"
        A [Duration String](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#hist-duration)
        that specifies how far back in time you want to fetch data.
    barSizeSetting: "1 hour"
        A [Bar Size](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#hist-bar-size)
        that specifies how fine-grained you want your historical data to be
        (daily, weekly, every 30 seconds, etc).
    whatToShow: "Trades"
        You may select from any of the [Historical Data Types](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#historical-whattoshow)
        but for most cases you'll probably be happy with one of "BID_ASK",
        "MIDPOINT", or "TRADES".
    useRTH: True
        "Use Regular Trading Hours". Set to `False` if you want the historical
        data to include after-hours/pre-market trading
    host: '127.0.0.1'
        Address of a running IBKR client (such as TWS or IBG) that has been
        configured to accept API connections
    port: 7497
        Port of a running IBKR client
    client_id: 9999
        Client ID you want to use for the request. If you are connecting to a
        system that is used by multiple users, then you may wish to set aside an
         ID for this purpose; if you're the only one using the account then
         you probably don't have to worry about it -- just use the default.
    timeout: 3
        Time in seconds to wait for a response.

    Examples
    --------
    ```
    {{< include ../examples/fetch_historical_data.py >}}
    ```
    """

    ib_conn = create_ibkr_socket_conn(
        host=host, port=port, client_id=client_id
    )
    ib_socket = ib_conn['ib_socket']

    send_ib_message(
        s=ib_socket,
        msg=req_historical_data(
            reqId=1,
            contract=contract,
            endDateTime=endDateTime,
            durationStr=durationStr,
            barSizeSetting=barSizeSetting,
            whatToShow=whatToShow,
            useRTH=useRTH,
            formatDate=2,
            keepUpToDate=False
        )
    )

    historical_data = None

    start_time = datetime.now()
    while (datetime.now() - start_time).seconds <= timeout:
        incoming_msg = read_ib_msg(sock=ib_socket)
        if incoming_msg[0] == '4' and incoming_msg[3] in ['162', '321']:
            warnings.warn(incoming_msg[4])
            break
        if incoming_msg[0] == functionary['incoming_msg_codes'][
            'HISTORICAL_DATA'
        ]:
            historical_data = format_historical_data_input(incoming_msg[1:])
            break

    ib_socket.close()

    return historical_data


def fetch_matching_symbols(
        pattern: str,
        host='127.0.0.1',
        port=7497,
        client_id=9999
):
    """Fetch assets whose symbol loosely matches a pattern

    Parameters
    -------------
    pattern: str
        A string, like "AAPL", "S&P 500" or "Vanguard" that you'd like to
        search for
    host: '127.0.0.1'
        Address of a running IBKR client (such as TWS or IBG) that has been
        configured to accept API connections
    port: 7497
        Port of a running IBKR client
    client_id: 9999
        Client ID you want to use for the request. If you are connecting to a
        system that is used by multiple users, then you may wish to set aside an
         ID for this purpose; if you're the only one using the account then
        you probably don't have to worry about it -- just use the default.

    Examples
    --------
    ```
    {{< include ../examples/fetch_matching_symbols.py >}}
    ```
    """

    ib_conn = create_ibkr_socket_conn(
        host=host, port=port, client_id=client_id
    )
    ib_socket = ib_conn['ib_socket']

    send_ib_message(
        s=ib_socket, msg=req_matching_symbols(reqId=1, pattern=pattern)
    )

    while True:
        incoming_msg = read_ib_msg(sock=ib_socket)
        if incoming_msg[0] == functionary['incoming_msg_codes'][
            'SYMBOL_SAMPLES'
        ]:
            matching_symbols = format_symbol_samples_input(incoming_msg[3:])
            break

    ib_socket.close()

    return matching_symbols

