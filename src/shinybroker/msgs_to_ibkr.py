from shinybroker.functionary import functionary
from shinybroker.utils import pack_message
from shinybroker.obj_defs import Contract


def req_contract_details(reqId: str, contract: Contract):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_CONTRACT_DATA'] + "\0" +
        "8\0" +  # VERSION
        reqId + "\0" +
        contract.conId + "\0" +  # srv v37 and above
        contract.symbol + "\0" +
        contract.secType + "\0" +
        contract.lastTradeDateOrContractMonth + "\0" +
        contract.strike + "\0" +
        contract.right + "\0" +
        contract.multiplier + "\0" +
        contract.exchange + "\0" +
        contract.primaryExchange + "\0" +
        contract.currency + "\0" +
        contract.localSymbol + "\0" +
        contract.tradingClass + "\0" +
        contract.includeExpired + "\0" +
        contract.secIdType + "\0" +
        contract.secId + "\0" +
        contract.issuerId  + "\0"
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
        snapshot: str,
        regulatorySnapshot: str,
        mktDataOptions: str
):

    VERSION = 11

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
            genericTickList + "\0" + # srv v31 and above
            snapshot + "\0" +
            regulatorySnapshot + "\0" +
            mktDataOptions + "\0"
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
