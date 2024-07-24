from shinybroker.functionary import functionary
from shinybroker.utils import pack_message, pack_element
from shinybroker.obj_defs import Contract


def req_contract_details(reqId: int, contract: Contract):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_CONTRACT_DATA'] + "\0" +
        "8\0" +  # VERSION
        pack_element(reqId) +
        pack_element(contract.conId) +  # srv v37 and above
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
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_CURRENT_TIME'] + "\0" +
        "1\0"  # VERSION
    )


def req_market_data_type(marketDataType: int):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_MARKET_DATA_TYPE'] + "\0" +
        "1\0" +  # VERSION
        pack_element(marketDataType)
    )


def req_matching_symbols(reqId: int, pattern: str):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_MATCHING_SYMBOLS'] + "\0" +
        pack_element(reqId) + 
        pack_element(pattern)
    )


def req_mkt_data(
        reqId: int,
        contract: Contract,
        genericTickList: str,
        snapshot: bool,
        regulatorySnapshot: bool,
        mktDataOptions: str
):

    # send req mkt data msg
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
            pack_element(contract.primaryExchange) + # srv v14 and above
            pack_element(contract.currency) +
            pack_element(contract.localSymbol) +
            pack_element(contract.tradingClass)
    )

    # Send combo legs for BAG requests (srv v8 and above)
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
            pack_element(genericTickList) +  # srv v31 and above
            pack_element(snapshot) +
            pack_element(regulatorySnapshot) +
            pack_element(mktDataOptions)
    )

    return pack_message(msg)


def req_sec_def_opt_params(
        reqId: str,
        underlyingSymbol: str,
        futFopExchange: str,
        underlyingSecType: str,
        underlyingConId: int
):
    return pack_message(
        functionary['outgoing_msg_codes'][
            'REQ_SEC_DEF_OPT_PARAMS'
        ] + "\0" +
        pack_element(reqId) +
        pack_element(underlyingSymbol) +
        pack_element(futFopExchange) +
        pack_element(underlyingSecType) +
        pack_element(underlyingConId)
    )


def req_ids(numIds:int):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_IDS'] + "\0" +
        "1\0" +  # VERSION
        pack_element(numIds)
    )
