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


def req_market_data_type(marketDataType: str):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_MARKET_DATA_TYPE'] + "\0" +
        "1\0" +  # VERSION
        marketDataType + "\0"
    )


def req_matching_symbols(reqId: str, pattern: str):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_MATCHING_SYMBOLS'] + "\0" +
        reqId + "\0" +
        pattern + "\0"
    )


def req_mkt_data(
        reqId: str,
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
            reqId + "\0" +
            contract.conId + "\0" +
            contract.symbol + "\0" +
            contract.secType + "\0" +
            contract.lastTradeDateOrContractMonth + "\0" +
            contract.strike + "\0" +
            contract.right + "\0" +
            contract.multiplier + "\0" +
            contract.exchange + "\0" +
            contract.primaryExchange + "\0" + # srv v14 and above
            contract.currency + "\0" +
            contract.localSymbol + "\0" +
            contract.tradingClass + "\0"
    )

    # Send combo legs for BAG requests (srv v8 and above)
    if contract.secType == "BAG":
        comboLegsCount = len(contract.comboLegs) if contract.comboLegs else 0
        for comboLeg in contract.comboLegs:
            msg += (
                    comboLeg.conId + "\0" +
                    comboLeg.ratio + "\0" +
                    comboLeg.action + "\0" +
                    comboLeg.exchange + "\0"
            )

    if contract.deltaNeutralContract:
        msg += (
                "1\0" +
                contract.deltaNeutralContract.conId + "\0" +
                contract.deltaNeutralContract.delta + "\0" +
                contract.deltaNeutralContract.price + "\0"
        )
    else:
        msg += "0\0"

    msg += (
            str(genericTickList) + "\0" + # srv v31 and above
            str(snapshot) + "\0" +
            str(regulatorySnapshot) + "\0" +
            str(mktDataOptions) + "\0"
    )

    return pack_message(msg)


def req_sec_def_opt_params(
        reqId:str,
        underlyingSymbol:str,
        futFopExchange:str,
        underlyingSecType:str,
        underlyingConId:str
):
    return pack_message(
        functionary['outgoing_msg_codes'][
            'REQ_SEC_DEF_OPT_PARAMS'
        ] + "\0" +
        reqId + "\0" +
        underlyingSymbol + "\0" +
        futFopExchange + "\0" +
        underlyingSecType + "\0" +
        underlyingConId + "\0"
    )


def req_ids(numIds:int):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_IDS'] + "\0" +
        "1\0" +  # VERSION
        str(numIds) + "\0"
    )
