import select
from shiny import reactive
from shinybroker.obj_defs import *
from shinybroker.msgs_to_ibkr import req_mkt_data


def start_mkt_data_subscription(
        market_data=None,
        mkt_data_socket=None,
        subscription_id=None,
        contract=Contract({}),
        genericTickList='',
        snapshot=False,
        regulatorySnapshot=False,
        mktDataOptions=''
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
            regulatorySnapshot=regulatorySnapshot,
            mktDataOptions=mktDataOptions
        )
    )
    mkt_dta.update({subscription_id: contract.compact()})
    market_data.set(mkt_dta.copy())

    # print('hello')
    #
    # mkt_dta = market_data()
    #
    # if subscription_id is None:
    #     try:
    #         subscription_id = max(list(map(int, mkt_dta.keys()))) + 1
    #     except ValueError:
    #         subscription_id = 1
    #     subscription_id = str(subscription_id)
    #
    # (rd, wt, er) = select.select([], [mkt_data_socket], [])
    # wt[0].send(
    #     req_mkt_data(
    #         reqId=subscription_id,
    #         contract=contract,
    #         genericTickList=genericTickList,
    #         snapshot=snapshot,
    #         regulatorySnapshot=regulatorySnapshot,
    #         mktDataOptions=mktDataOptions
    #     )
    # )
    # mkt_dta.update({subscription_id: contract.compact()})
    # exec('market_data.set(mkt_dta.copy())')
