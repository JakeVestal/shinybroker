import select
from shiny import reactive
from shinybroker.obj_defs import *
from shinybroker.msgs_to_ibkr import req_mkt_data, req_historical_data


def start_mkt_data_subscription(
        market_data=None,
        mkt_data_socket=None,
        subscription_id=None,
        contract=Contract({}),
        genericTickList='',
        snapshot=False,
        regulatorySnapshot=False
):
    mkt_dta = market_data()

    if subscription_id is None:
        try:
            subscription_id = max(list(map(int, mkt_dta.keys()))) + 1
        except ValueError:
            subscription_id = 1

    subscription_id = str(subscription_id)

    (rd, wt, er) = select.select([], [mkt_data_socket], [])
    wt[0].send(
        req_mkt_data(
            reqId=int(subscription_id),
            contract=contract,
            genericTickList=genericTickList,
            snapshot=snapshot,
            regulatorySnapshot=regulatorySnapshot
        )
    )
    mkt_dta.update({subscription_id: contract.compact()})
    market_data.set(mkt_dta.copy())

def start_historical_data_subscription(
        historical_data=None,
        hd_socket=None,
        subscription_id=None,
        contract=Contract({}),
        endDateTime="",
        durationStr="1 D",
        barSizeSetting='1 hour',
        whatToShow='Trades',
        useRTH=1,
        formatDate=1,
        keepUpToDate=0
):
    """Reactively get historical data

    Creates a subscription for historical data using the parameters supplied.
    Results will appear in the `sb_rvs['historical_data']` object, where they
    are accessible by other functions in your app.

    Parameters
    ----------
    historical_data: None
        You probably want to pass `sb_rvs['historical_data']` to this parameter
        unless you have declared a different reactive variable for storing your
        historical data queries. Unless you have a very specific use case to
        do otherwise, use `sb_rvs['historical_data']`.
    hd_socket: None
        The socket on which you want to make the historical data subscription.
        You almost certainly want to pass `ib_socket` as this parameter unless
        you have constructed an app that uses different sockets for different
        tasks. This is not recommended except for advanced use cases.
    subscription_id: None
        Identifier of the request. You may use your own system, such as using
        contract `symbol` as your ID if you wish. If not supplied, then
        ShinyBroker will assign the smallest number that isn't already in use
        as a historical data subscription ID.
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

    Example
    -----------
    Run the app below for an informative exploration of this function and
    related objects.
    ```
    {{< include ../examples/start_historical_data_subscription.py >}}
    ```

    """
    hd = historical_data()

    if subscription_id is None:
        try:
            subscription_id = max(list(map(int, hd.keys()))) + 1
        except ValueError:
            subscription_id = 1

    subscription_id = str(subscription_id)

    (rd, wt, er) = select.select([], [hd_socket], [])
    wt[0].send(
        req_historical_data(
            reqId=int(subscription_id),
            contract=contract,
            endDateTime=endDateTime,
            durationStr=durationStr,
            barSizeSetting=barSizeSetting,
            whatToShow=whatToShow,
            useRTH=useRTH,
            formatDate=formatDate,
            keepUpToDate=keepUpToDate
        )
    )
    hd.update({subscription_id: contract.compact()})
    historical_data.set(hd.copy())
