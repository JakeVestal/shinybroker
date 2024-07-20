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


    # def req_mkt_data(
    #         reqId: TickerId,
    #         contract: Contract,
    #         genericTickList: str,
    #         snapshot: bool,
    #         regulatorySnapshot: bool,
    #         mktDataOptions: TagValueList
    # ):
    #
    #     VERSION = 11
    #
    #     # send req mkt data msg
    #     flds = []
    #     flds += [make_field(OUT.REQ_MKT_DATA),
    #              make_field(VERSION),
    #              make_field(reqId),
    #              make_field(contract.conId),
    #              make_field(contract.symbol),
    #              make_field(contract.secType),
    #              make_field(contract.lastTradeDateOrContractMonth),
    #              make_field(contract.strike),
    #              make_field(contract.right),
    #              make_field(contract.multiplier),  # srv v15 and above
    #              make_field(contract.exchange),
    #              make_field(contract.primaryExchange),  # srv v14 and above
    #              make_field(contract.currency),
    #              make_field(contract.localSymbol),
    #              make_field(contract.tradingClass)]
    #
    #     # Send combo legs for BAG requests (srv v8 and above)
    #     if contract.secType == "BAG":
    #         comboLegsCount = len(
    #             contract.comboLegs) if contract.comboLegs else 0
    #         flds += [make_field(comboLegsCount), ]
    #         for comboLeg in contract.comboLegs:
    #             flds += [make_field(comboLeg.conId),
    #                      make_field(comboLeg.ratio),
    #                      make_field(comboLeg.action),
    #                      make_field(comboLeg.exchange)]
    #
    #     if contract.deltaNeutralContract:
    #         flds += [make_field(True),
    #                  make_field(contract.deltaNeutralContract.conId),
    #                  make_field(contract.deltaNeutralContract.delta),
    #                  make_field(contract.deltaNeutralContract.price)]
    #     else:
    #         flds += [make_field(False)]
    #
    #     flds += [make_field(genericTickList),  # srv v31 and above
    #              make_field(snapshot),
    #              make_field(regulatorySnapshot),
    #              make_field(mktDataOptions)]
    #
    #     return make_msg("".join(flds))


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
