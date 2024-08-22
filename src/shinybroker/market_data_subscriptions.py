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
