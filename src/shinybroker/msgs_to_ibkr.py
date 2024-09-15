from shinybroker.functionary import functionary
from shinybroker.utils import pack_message, pack_element
from shinybroker.obj_defs import Contract


def req_contract_details(reqId: int, contract: Contract):
    """Create a contract details request string

    Parameters
    -----------
    reqId: int
        Numeric identifier of the request
    contract: Contract
        A [Contract](`shinybroker.Contract`) object

    Examples
    -----------
    ```
    import shinybroker as sb
    req_contract_details_msg = sb.req_contract_details(
        reqId=1,
        contract=Contract({
            'symbol': "AAPL",
            'secType': "STK",
            'exchange': "SMART",
            'currency': "USD"
        })
    )
    print(req_contract_details_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_CONTRACT_DATA'] + "\0" +
        "8\0" +  # VERSION
        pack_element(reqId) +
        pack_element(contract.conId) +
        pack_element(contract.symbol) +
        pack_element(contract.secType) +
        pack_element(contract.lastTradeDateOrContractMonth) +
        pack_element(contract.strike) +
        pack_element(contract.right) +
        pack_element(contract.multiplier) +
        pack_element(contract.exchange) +
        pack_element(contract.primaryExchange) +
        pack_element(contract.currency) +
        pack_element(contract.localSymbol) +
        pack_element(contract.tradingClass) +
        pack_element(contract.includeExpired) +
        pack_element(contract.secIdType) +
        pack_element(contract.secId) +
        pack_element(contract.issuerId)
    )


def req_current_time():
    """Create a request string for the current broker time

    Examples
    -----------
    ```
    import shinybroker as sb
    req_current_time_msg = sb.req_current_time()
    print(req_current_time_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_CURRENT_TIME'] + "\0" +
        "1\0"  # VERSION
    )


def req_market_data_type(marketDataType: int):
    """Create a string for setting your session's market data type

    Parameters
    -------------
    marketDataType: int
        Integer identifier for the [market data type](
        https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#md-type-behavior
        ) that you want

    Examples
    -----------
    ```
    import shinybroker as sb
    # create a request string for setting the market data type to "DELAYED"
    req_market_data_type_msg = sb.req_market_data_type(3)
    print(req_market_data_type_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_MARKET_DATA_TYPE'] + "\0" +
        "1\0" +  # VERSION
        pack_element(marketDataType)
    )


def req_matching_symbols(reqId: int, pattern: str):
    """Create a request string for symbols that loosely match a pattern

    Parameters
    -------------
    reqId: int
        Numeric identifier of the request
    pattern: str
        A string, like "AAPL", "S&P 500" or "Vanguard" that you'd like to
        search for

    Examples
    ---------------
    ```
    import shinybroker as sb
    req_matching_symbols_msg = sb.req_market_data_type(3)
    print(req_matching_symbols_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_MATCHING_SYMBOLS'] + "\0" +
        pack_element(reqId) +
        pack_element(pattern)
    )


def req_mkt_data(
        reqId: int,
        contract: Contract,
        genericTickList="",
        snapshot=False,
        regulatorySnapshot=False
):
    """Create a market data request string

    Parameters
    ---------------
    reqId: int
        Numeric identifier of the request
    contract: Contract
        A [Contract](`shinybroker.Contract`) object
    genericTickList: ""
        Comma-separated string of the numerical [Generic Ticks](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#available-tick-types)
        for which you'd like data
    snapshot: False
        Set to `True` if you want a [snapshot](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#streaming-data-snapshot)
    regulatorySnapshot: False
        Set to `True` if you want a [regulatory snapshot](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#regulatory-snapshot)

    Examples
    -----------
    ```
    import shinybroker as sb
    mkt_data_req_msg = sb.req_mkt_data(
        reqId=1,
        contract=sb.Contract({
            'symbol': 'AAPL',
            'secType': 'STK',
            'exchange': 'SMART',
            'currency': 'USD'
        }),
        genericTickList="233,236"  # request for "RT Volume" & "Shortable"
    )
    print(mkt_data_req_msg)
    ```
    """
    msg = (
            functionary['outgoing_msg_codes']['REQ_MKT_DATA'] + "\0" +
            "11\0" +  # VERSION
            pack_element(reqId) +
            pack_element(contract.conId) +
            pack_element(contract.symbol) +
            pack_element(contract.secType) +
            pack_element(contract.lastTradeDateOrContractMonth) +
            pack_element(contract.strike) +
            pack_element(contract.right) +
            pack_element(contract.multiplier) +
            pack_element(contract.exchange) +
            pack_element(contract.primaryExchange) +
            pack_element(contract.currency) +
            pack_element(contract.localSymbol) +
            pack_element(contract.tradingClass)
    )

    if contract.secType == "BAG":
        comboLegsCount = len(contract.comboLegs) if contract.comboLegs else 0
        for comboLeg in contract.comboLegs:
            msg += (
                    pack_element(comboLeg.conId) +
                    pack_element(comboLeg.ratio) +
                    pack_element(comboLeg.action) +
                    pack_element(comboLeg.exchange)
            )

    if contract.deltaNeutralContract:
        msg += (
                "1\0" +
                pack_element(contract.deltaNeutralContract.conId) +
                pack_element(contract.deltaNeutralContract.delta) +
                pack_element(contract.deltaNeutralContract.price)
        )
    else:
        msg += "0\0"

    msg += (
            pack_element(genericTickList) +
            pack_element(snapshot) +
            pack_element(regulatorySnapshot) +
            pack_element('')
    )

    return pack_message(msg)


def cancel_mkt_data(reqId: int):
    """Create a message to cancel an existing market data subscription by ID

    Parameters
    ------------
    reqId: int
        Numeric identifier of the market data request you want to cancel

    Examples
    ------------
    ```
    import shinybroker as sb
    # create message to cancel the market data subscription whose id is 1
    cancel_mkt_data_msg = sb.cancel_mkt_data(1)
    print(cancel_mkt_data_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes']['CANCEL_MKT_DATA'] + "\0" +
        "2\0" +  # VERSION
        pack_element(reqId)
    )


def req_sec_def_opt_params(
        reqId: int,
        underlyingConId: int,
        underlyingSymbol: str,
        underlyingSecType: str,
        futFopExchange=""
):
    """Create a request for the security-defined option parameters of a security

    Parameters
    ------------
    reqId: int
        Numeric identifier of the request
    underlyingConId: int
        `conId` of the underlying security
    underlyingSymbol: ""
        Symbol of the underlying security for which you want option parameters.
    underlyingSecType: ""
        Type of the underlying security; e.g., "`STK`"
    futFopExchange: ""
        Only set this parameter if the underlying is a futures contract; in
        other words, don't change it from the default `""` if your underlying is
         a stock. If your underlying **is** a futures contract, then use
         `futFopExchange` to specify the exchange for which you want option
         parameters. You may still pass in `""` if you want the results to
         include **all** of the exchanges available at IBKR that trade
         options on your specified underlying.

    Examples
    --------
    ```
    import shinybroker as sb
    # You can specify contract id only
    req_sec_def_opt_params_msg = sb.req_sec_def_opt_params(
        reqId=1,
        underlyingConId=265598
    )
    print(req_sec_def_opt_params_msg)
    req_sec_def_opt_params_msg = sb.req_sec_def_opt_params(
        reqId=1,
        underlyingSymbol="AAPL",
        futFopExchange="",
        underlyingSecType="STK",
        underlyingConId=265598
    )
    print(req_sec_def_opt_params_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes'][
            'REQ_SEC_DEF_OPT_PARAMS'
        ] + "\0" +
        pack_element(reqId) +
        pack_element(underlyingSymbol) +
        pack_element(futFopExchange) +
        pack_element(underlyingSecType) +
        pack_element(underlyingConId) +
        pack_element(futFopExchange)
    )


def req_ids(numIds:int):
    """Create a request for the next valid numeric ID that can be used to
    create a trade order

    Parameter
    ------------
    numIds: int
        Specifies how many valid IDs you want in the result

    Examples
    ---------
    ```
    import shinybroker as sb
    # create a message that asks for 10 valid IDs
    req_ids_msg = sb.req_ids(10)
    print(req_ids_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_IDS'] + "\0" +
        "1\0" +  # VERSION
        pack_element(numIds)
    )


def req_historical_data(
        reqId: int,
        contract: Contract,
        endDateTime="",
        durationStr="1 D",
        barSizeSetting='1 hour',
        whatToShow='Trades',
        useRTH=True,
        formatDate=1,
        keepUpToDate=False
):
    """Create a request for the historical data of a financial instrument

    Parameters
    ----------
    reqId: int
        Numeric identifier of the request
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
    formatDate: 1
        Numeric code from the [Format Date Received](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#hist-format-date)
        table that specifies how you want your dates formatted in the data.
    keepUpToDate: False
        Set to `True` if you want to keep receiving new bar data as it
        becomes available. For a `barSizeSetting` of `5 min`, that would mean
        you receive new data every 5 minutes.

    Examples
    ------------
    ```
    import shinybroker as sb
    # create a request for historical TRADES of AAPL for the last 30 days,
    #   starting today. Report the data on a daily basis, regular trading
    #   hours only, and format it as "string time zone date". Make it a one-time
    #   query; don't keep it up-to-date.
    req_historical_data_msg = sb.req_historical_data(
        reqId=1,
        contract = Contract({
            'symbol': "AAPL",
            'secType': "STK",
            'exchange': "SMART",
            'currency': "USD"
        }),
        durationStr='30 D',
        barSizeSetting='1 day'
    )
    print(req_historical_data_msg)
    ```
    """
    msg = (
            functionary['outgoing_msg_codes']['REQ_HISTORICAL_DATA'] + "\0" +
            pack_element(reqId) +
            pack_element(contract.conId) +
            pack_element(contract.symbol) +
            pack_element(contract.secType) +
            pack_element(contract.lastTradeDateOrContractMonth) +
            pack_element(contract.strike) +
            pack_element(contract.right) +
            pack_element(contract.multiplier) +
            pack_element(contract.exchange) +
            pack_element(contract.primaryExchange) +
            pack_element(contract.currency) +
            pack_element(contract.localSymbol) +
            pack_element(contract.tradingClass) +
            pack_element(contract.includeExpired) +
            pack_element(endDateTime) +
            pack_element(barSizeSetting) +
            pack_element(durationStr) +
            pack_element(useRTH) +
            pack_element(whatToShow) +
            pack_element(formatDate)
    )

    # Send combo legs for BAG requests
    if contract.secType == "BAG":
        msg += pack_element(len(contract.comboLegs))
        for comboLeg in contract.comboLegs:
            msg += (
                    pack_element(comboLeg.conId) +
                    pack_element(comboLeg.ratio) +
                    pack_element(comboLeg.action) +
                    pack_element(comboLeg.exchange)
            )

    msg += (
            pack_element(keepUpToDate) +
            "\x00"  # chartOptionsStr not used in ShinyBroker
    )

    return pack_message(msg)


def cancel_historical_data(reqId: int):
    """Create a message that will cancel an existing historical data request.

    Parameters
    ----------
    reqId: int
        The numerical ID of the historical data request you want to cancel.

    Examples
    ----------
    ```
    import shinybroker as sb
    # Message that will cancel historical data request having ID of 1
    cancel_historical_data_msg = sb.cancel_historical_data(1)
    print(cancel_historical_data_msg)
    ```
    """
    return pack_message(
        functionary['outgoing_msg_codes']['CANCEL_HISTORICAL_DATA'] + "\0" +
        "1\0" +  # VERSION
        pack_element(reqId)
    )

def req_real_time_bars(
        reqId: int,
        contract: Contract,
        whatToShow="TRADES",
        useRTH=0
):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_REAL_TIME_BARS'] + "\0" +
        "3\0" +  # VERSION
        pack_element(reqId) +
        pack_element(contract.conId) +
        pack_element(contract.symbol) +
        pack_element(contract.secType) +
        pack_element(contract.lastTradeDateOrContractMonth) +
        pack_element(contract.strike) +
        pack_element(contract.right) +
        pack_element(contract.multiplier) +
        pack_element(contract.exchange) +
        pack_element(contract.primaryExchange) +
        pack_element(contract.currency) +
        pack_element(contract.localSymbol) +
        pack_element(contract.tradingClass) +
        pack_element(5) +  # barSize, not yet implemented by IBKR
        pack_element(whatToShow) +
        pack_element(useRTH) +
        pack_element("")  # realTimeBarOptions, not yet implemented by IBKR
    )


def cancel_real_time_bars(reqId: int):
    return pack_message(
        functionary['outgoing_msg_codes']['CANCEL_REAL_TIME_BARS'] + "\0" +
        "1\0" +  # VERSION
        pack_element(reqId)
    )


def req_scanner_parameters():
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_SCANNER_PARAMS'] + "\0" +
        "1\0"  # VERSION
    )


