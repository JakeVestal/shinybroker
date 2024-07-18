from shinybroker.functionary import functionary
from shinybroker.utils import pack_message

# def req_contract_details(reqId:int, contract:Contract):
#     VERSION = 8
#
#     return make_msg(
#         "".join(
#             [
#                 make_field(
#                     functionary['outgoing_msg_codes']['REQ_CONTRACT_DATA']
#                 ),
#                 make_field(VERSION),
#                 make_field(reqId),
#                 make_field(contract.conId),  # srv v37 and above
#                 make_field(contract.symbol),
#                 make_field(contract.secType),
#                 make_field(contract.lastTradeDateOrContractMonth),
#                 make_field(contract.strike),
#                 make_field(contract.right),
#                 make_field(contract.multiplier),
#                 make_field(contract.exchange),
#                 make_field(contract.primaryExchange),
#                 make_field(contract.currency),
#                 make_field(contract.localSymbol),
#                 make_field(contract.tradingClass),
#                 make_field(contract.includeExpired),
#                 make_field(contract.secIdType),
#                 make_field(contract.secId),
#                 make_field(contract.issuerId)
#             ]
#         )
#     )


def req_current_time():
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_CURRENT_TIME'] + "\0" +
        "1\0"  # VERSION
    )


def req_market_data_type(marketDataType: str):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_MARKET_DATA_TYPE'] +
        "1\0" +  # VERSION
        marketDataType + "\0"
    )


# def req_matching_symbols(reqId: TickerId, pattern: str):
#     return make_msg(
#         make_field(OUT.REQ_MATCHING_SYMBOLS) +
#         make_field(reqId) +
#         make_field(pattern)
#     )
#
#
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
#
#
# def req_sec_def_opt_params(
#         reqId:int,
#         underlyingSymbol:str,
#         futFopExchange:str,
#         underlyingSecType:str,
#         underlyingConId:int
# ):
#     return make_msg(
#         "".join(
#             [
#                 make_field(OUT.REQ_SEC_DEF_OPT_PARAMS),
#                 make_field(reqId),
#                 make_field(underlyingSymbol),
#                 make_field(futFopExchange),
#                 make_field(underlyingSecType),
#                 make_field(underlyingConId)
#             ]
#         )
#     )


def req_ids(numIds:int):
    return pack_message(
        functionary['outgoing_msg_codes']['REQ_IDS'] + "\0" +
        "1\0" +  # VERSION
        str(numIds) + "\0"
    )
