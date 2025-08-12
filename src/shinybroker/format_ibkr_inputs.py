import warnings

import pandas as pd

from datetime import datetime
from shinybroker.utils import formatter2


def format_historical_data_input(hst_dta):
    hd_len = len(hst_dta)

    if len(hst_dta[4]) == 8:
        timestamps = [
            datetime(
                int(hst_dta[i][:4]),
                int(hst_dta[i][4:6]),
                int(hst_dta[i][6:8])
            ).date() for i in range(4, hd_len, 8)
        ]
    else:
        timestamps = [
            datetime.fromtimestamp(
                int(hst_dta[i])
            ) for i in range(4, hd_len, 8)
        ]

    def vem_try():
        try:
            volume = [int(hst_dta[i]) for i in range(9, hd_len, 8)]
        except ValueError:
            volume = [float(hst_dta[i]) for i in range(9, hd_len, 8)]
        return volume

    def bc_try(x):
        try:
            bc = int(x)
        except ValueError:
            bc = 0
        return bc


    return {
        'startDateStr': hst_dta[1],
        'endDateStr': hst_dta[2],
        'hst_dta': pd.DataFrame({
            'timestamp': timestamps,
            'open': [float(hst_dta[i]) for i in range(5, hd_len, 8)],
            'high': [float(hst_dta[i]) for i in range(6, hd_len, 8)],
            'low': [float(hst_dta[i]) for i in range(7, hd_len, 8)],
            'close': [float(hst_dta[i]) for i in range(8, hd_len, 8)],
            'volume': vem_try(),
            'wap': [
                round(float(hst_dta[i]), 3) for i in range(10, hd_len, 8)
            ],
            'barCount': [bc_try(hst_dta[i]) for i in range(11, hd_len, 8)]
        })
    }


def format_sec_def_opt_params_input(sdop):
    n_expiries = int(sdop[4])
    return pd.DataFrame({
        'exchange': [sdop[0]],
        'underlying_con_id': [sdop[1]],
        'trading_class': [sdop[2]],
        'multiplier': [sdop[3]],
        'expirations': ",".join(sdop[5:5 + n_expiries]),
        'strikes': ",".join(
            sdop[6 + n_expiries:len(sdop)]
        )
    })


def format_symbol_samples_input(symbol_samples):

    bonds = []

    while True:
        try:
            bond_ind = symbol_samples.index('-1')
            bonds.append(
                pd.DataFrame.from_dict({
                    'issuer': [symbol_samples[bond_ind + 3]],
                    'issuer_id': [symbol_samples[bond_ind + 4]]
                })
            )
            del symbol_samples[bond_ind:bond_ind + 5]
        except ValueError:
            break

    stocks = []

    while True:
        try:
            n_derivative_contracts = int(symbol_samples[5])
            stocks.append(
                pd.DataFrame.from_dict({
                    'con_id': [symbol_samples[0]],
                    'symbol': [symbol_samples[1]],
                    'sec_type': [symbol_samples[2]],
                    'primary_exchange': [symbol_samples[3]],
                    'currency': [symbol_samples[4]],
                    'derivative_sec_types': ",".join(
                        symbol_samples[6:5 + n_derivative_contracts]
                    ),
                    'description': [
                        symbol_samples[6 + n_derivative_contracts]]
                })
            )
            del symbol_samples[:7 + n_derivative_contracts]
        except IndexError:
            break

    if not bonds:
        bonds = pd.DataFrame({})
    else:
        bonds = pd.concat(bonds, ignore_index=True)

    if not stocks:
        stocks = pd.DataFrame({})
    else:
        stocks = pd.concat(stocks, ignore_index=True)

    return {'stocks': stocks, 'bonds': bonds}


def format_contract_details(cdeets):
    contract_details_lst = []

    # print("processing contract details")
    # print(type(cdeets))
    # print(f"cdeets = {cdeets}")


    for i in range(len(cdeets)):
        if cdeets[i][0] == 'BOND':
            end_of_sec_id_list_ind = 13 + 2 * int(cdeets[i][12])
            contract_details_lst.append(
                pd.DataFrame({
                    'symbol': [cdeets[i][4]],
                    'underSymbol': [cdeets[i][6]],
                    'conId': [cdeets[i][7]],
                    'minTick': [cdeets[i][8]],
                    'orderTypes': [cdeets[i][9]],
                    'validExchanges': [cdeets[i][10]],
                    'secIdList': ["{" + ",".join([
                        "'" + "':'".join(cdeets[i][x:(x + 2)]) + "'" for
                        x in range(13, end_of_sec_id_list_ind, 2)
                    ]) + "}"],
                    'aggGroup': [cdeets[i][end_of_sec_id_list_ind]],
                    'marketRuleIds': [cdeets[i][end_of_sec_id_list_ind + 1]],
                    'minSize': [cdeets[i][end_of_sec_id_list_ind + 2]],
                    'sizeIncrement': [
                        cdeets[i][end_of_sec_id_list_ind + 3]
                    ],
                    'suggestedSizeIncrement': [
                        cdeets[i][end_of_sec_id_list_ind + 4]
                    ]
                })
            )
            continue
        match cdeets[i][1]:
            case 'CASH':
                contract_details_lst.append(
                    pd.DataFrame({
                        'symbol': [cdeets[i][0]],
                        'secType': [cdeets[i][1]],
                        'exchange': [cdeets[i][3]],
                        'currency': [cdeets[i][4]],
                        'localSymbol': [cdeets[i][5]],
                        'marketName': [cdeets[i][6]],
                        'tradingClass': [cdeets[i][7]],
                        'conId': [cdeets[i][8]],
                        'minTick': [cdeets[i][9]],
                        'orderTypes': [cdeets[i][10]],
                        'validExchanges': [cdeets[i][11]],
                        'priceMagnifier': [cdeets[i][12]],
                        'longName': [cdeets[i][14]],
                        'timeZoneId': [cdeets[i][15]],
                        'tradingHours': [cdeets[i][16]],
                        'liquidHours': [cdeets[i][17]],
                        'aggGroup': [cdeets[i][19]],
                        'marketRuleIds': [cdeets[i][20]],
                        'minSize': [cdeets[i][21]],
                        'sizeIncrement': [cdeets[i][22]],
                        'suggestedSizeIncrement': [cdeets[i][23]]
                    })
                )
            case 'CMDTY':
                contract_details_lst.append(
                    pd.DataFrame({
                        'symbol': [cdeets[i][0]],
                        'secType': [cdeets[i][1]],
                        'exchange': [cdeets[i][3]],
                        'currency': [cdeets[i][4]],
                        'localSymbol': [cdeets[i][5]],
                        'marketName': [cdeets[i][6]],
                        'tradingClass': [cdeets[i][7]],
                        'conId': [cdeets[i][8]],
                        'minTick': [cdeets[i][9]],
                        'orderTypes': [cdeets[i][10]],
                        'validExchanges': [cdeets[i][11]],
                        'priceMagnifier': [cdeets[i][12]],
                        'longName': [cdeets[i][14]],
                        'timeZoneId': [cdeets[i][15]],
                        'tradingHours': [cdeets[i][16]],
                        'liquidHours': [cdeets[i][17]],
                        'evMultiplier': [cdeets[i][18]],
                        'aggGroup': [cdeets[i][19]],
                        'marketRuleIds': [cdeets[i][20]],
                        'minSize': [cdeets[i][21]],
                        'sizeIncrement': [cdeets[i][22]],
                        'suggestedSizeIncrement': [cdeets[i][23]]
                    })
                )
            case 'FUND':
                end_of_sec_id_list_ind = 19 + 2 * int(cdeets[i][18])
                contract_details_lst.append(
                    pd.DataFrame({
                        'symbol': [cdeets[i][0]],
                        'secType': [cdeets[i][1]],
                        'exchange': [cdeets[i][3]],
                        'currency': [cdeets[i][4]],
                        'localSymbol': [cdeets[i][5]],
                        'marketName': [cdeets[i][6]],
                        'tradingClass': [cdeets[i][7]],
                        'conId': [cdeets[i][8]],
                        'minTick': [cdeets[i][9]],
                        'orderTypes': [cdeets[i][10]],
                        'validExchanges': [cdeets[i][11]],
                        'priceMagnifier': [cdeets[i][12]],
                        'longName': [cdeets[i][14]],
                        'timeZoneId': [cdeets[i][15]],
                        'tradingHours': [cdeets[i][16]],
                        'liquidHours': [cdeets[i][17]],
                        'secIdList': ["{" + ",".join([
                            "'" + "':'".join(cdeets[i][x:(x + 2)]) + "'" for
                            x in range(19, end_of_sec_id_list_ind, 2)
                        ]) + "}"],
                        'marketRuleIds': [
                            cdeets[i][end_of_sec_id_list_ind + 1]
                        ],
                        'minSize': [
                            cdeets[i][end_of_sec_id_list_ind + 2]
                        ],
                        'sizeIncrement': [
                            cdeets[i][end_of_sec_id_list_ind + 3]
                        ],
                        'suggestedSizeIncrement': [
                            cdeets[i][end_of_sec_id_list_ind + 4]
                        ],
                        'fundName': [
                            cdeets[i][end_of_sec_id_list_ind + 5]
                        ],
                        'fundFamily': [
                            cdeets[i][end_of_sec_id_list_ind + 6]
                        ],
                        'fundFrontLoad': [
                            cdeets[i][end_of_sec_id_list_ind + 7]
                        ],
                        'fundBackLoad': [
                            cdeets[i][end_of_sec_id_list_ind + 8]
                        ],
                        'fundBackLoadTimeInterval': [
                            cdeets[i][end_of_sec_id_list_ind + 9]
                        ],
                        'fundManagementFee': [
                            cdeets[i][end_of_sec_id_list_ind + 10]
                        ],
                        'fundClosed': [
                            cdeets[i][end_of_sec_id_list_ind + 11]
                        ],
                        'fundClosedForNewInvestors': [
                            cdeets[i][end_of_sec_id_list_ind + 12]
                        ],
                        'fundClosedForNewMoney': [
                            cdeets[i][end_of_sec_id_list_ind + 13]
                        ],
                        'fundNotifyAmount': [
                            cdeets[i][end_of_sec_id_list_ind + 14]
                        ],
                        'fundMinimumInitialPurchase': [
                            cdeets[i][end_of_sec_id_list_ind + 15]
                        ],
                        'fundSubsequentMinimumPurchase': [
                            cdeets[i][end_of_sec_id_list_ind + 16]
                        ],
                        'fundBlueSkyStates': [
                            cdeets[i][end_of_sec_id_list_ind + 17]
                        ],
                        'fundBlueSkyTerritories': [
                            cdeets[i][end_of_sec_id_list_ind + 18]
                        ],
                        'ineligibilityReasonList': ["{" + ",".join([
                            "'" + "':'".join(cdeets[i][x:(x + 2)]) + "'" for
                            x in range(
                                end_of_sec_id_list_ind + 20,
                                len(cdeets[i]),
                                2
                            )
                        ]) + "}"]
                    })
                )
            case 'IND':
                contract_details_lst.append(
                    pd.DataFrame({
                        'symbol': [cdeets[i][0]],
                        'secType': [cdeets[i][1]],
                        'exchange': [cdeets[i][3]],
                        'currency': [cdeets[i][4]],
                        'localSymbol': [cdeets[i][5]],
                        'conId': [cdeets[i][6]],
                        'minTick': [cdeets[i][7]],
                        'orderTypes': [cdeets[i][8]],
                        'validExchanges': [cdeets[i][9]],
                        'priceMagnifier': [cdeets[i][10]],
                        'longName': [cdeets[i][12]],
                        'timeZoneId': [cdeets[i][13]],
                        'tradingHours': [cdeets[i][14]],
                        'liquidHours': [cdeets[i][15]],
                        'aggGroup': [cdeets[i][16]],
                        'underSymbol': [cdeets[i][17]],
                        'marketRuleIds': [cdeets[i][18]],
                        'minSize': [cdeets[i][19]],
                        'sizeIncrement': [cdeets[i][20]],
                        'suggestedSizeIncrement': [cdeets[i][21]]
                    })
                )
            case 'OPT':
                match len(cdeets[i]):
                    case 36:
                        contract_details_lst.append(
                            pd.DataFrame({
                                'symbol': [cdeets[i][0]],
                                'secType': [cdeets[i][1]],
                                'lastTradeDate': [cdeets[i][2]],
                                'strike': [cdeets[i][4]],
                                'right': [cdeets[i][5]],
                                'exchange': [cdeets[i][6]],
                                'currency': [cdeets[i][7]],
                                'localSymbol': [cdeets[i][8]],
                                'marketName': [cdeets[i][9]],
                                'tradingClass': [cdeets[i][10]],
                                'conId': [cdeets[i][11]],
                                'minTick': [cdeets[i][12]],
                                'multiplier': [cdeets[i][13]],
                                'orderTypes': [cdeets[i][14]],
                                'validExchanges': [cdeets[i][15]],
                                'priceMagnifier': [cdeets[i][16]],
                                'underConID': [cdeets[i][17]],
                                'longName': [cdeets[i][18]],
                                'contractMonth': [cdeets[i][19]],
                                'industry': [cdeets[i][20]],
                                'category': [cdeets[i][21]],
                                'subcategory': [cdeets[i][22]],
                                'timeZoneId': [cdeets[i][23]],
                                'tradingHours': [cdeets[i][24]],
                                'liquidHours': [cdeets[i][25]],
                                'aggGroup': [cdeets[i][26]],
                                'underSymbol': [cdeets[i][28]],
                                'underSecType': [cdeets[i][29]],
                                'marketRuleIds': [cdeets[i][30]],
                                'realExpirationDate': [cdeets[i][31]],
                                'minSize': [cdeets[i][32]],
                                'sizeIncrement': [cdeets[i][33]],
                                'suggestedSizeIncrement': [cdeets[i][34]]
                            })
                        )
                    case 34:
                        contract_details_lst.append(
                            pd.DataFrame({
                                'symbol': [cdeets[i][0]],
                                'secType': [cdeets[i][1]],
                                'lastTradeDate': [cdeets[i][2]],
                                'strike': [cdeets[i][3]],
                                'right': [cdeets[i][4]],
                                'exchange': [cdeets[i][5]],
                                'currency': [cdeets[i][6]],
                                'localSymbol': [cdeets[i][7]],
                                'marketName': [cdeets[i][8]],
                                'tradingClass': [cdeets[i][9]],
                                'conId': [cdeets[i][10]],
                                'minTick': [cdeets[i][11]],
                                'multiplier': [cdeets[i][12]],
                                'orderTypes': [cdeets[i][13]],
                                'validExchanges': [cdeets[i][14]],
                                'priceMagnifier': [cdeets[i][15]],
                                'underConID': [cdeets[i][16]],
                                'longName': [cdeets[i][17]],
                                'contractMonth': [cdeets[i][18]],
                                'industry': [cdeets[i][19]],
                                'category': [cdeets[i][20]],
                                'subcategory': [cdeets[i][21]],
                                'timeZoneId': [cdeets[i][22]],
                                'tradingHours': [cdeets[i][23]],
                                'liquidHours': [cdeets[i][24]],
                                'aggGroup': [cdeets[i][26]],
                                'underSymbol': [cdeets[i][27]],
                                'underSecType': [cdeets[i][28]],
                                'marketRuleIds': [cdeets[i][29]],
                                'realExpirationDate': [cdeets[i][30]],
                                'minSize': [cdeets[i][31]],
                                'sizeIncrement': [cdeets[i][32]],
                                'suggestedSizeIncrement': [cdeets[i][33]]
                            })
                        )
                    case 31:
                        contract_details_lst.append(
                            pd.DataFrame({
                                'symbol': [cdeets[i][0]],
                                'secType': [cdeets[i][1]],
                                'lastTradeDate': [cdeets[i][2]],
                                'strike': [cdeets[i][3]],
                                'right': [cdeets[i][4]],
                                'exchange': [cdeets[i][5]],
                                'currency': [cdeets[i][6]],
                                'localSymbol': [cdeets[i][7]],
                                'marketName': [cdeets[i][8]],
                                'tradingClass': [cdeets[i][9]],
                                'conId': [cdeets[i][10]],
                                'minTick': [cdeets[i][11]],
                                'multiplier': [cdeets[i][12]],
                                'orderTypes': [cdeets[i][13]],
                                'validExchanges': [cdeets[i][14]],
                                'priceMagnifier': [cdeets[i][15]],
                                'underConID': [cdeets[i][16]],
                                'longName': [cdeets[i][17]],
                                'contractMonth': [cdeets[i][18]],
                                'industry': [cdeets[i][19]],
                                'category': [cdeets[i][20]],
                                'subcategory': [cdeets[i][21]],
                                'aggGroup': [cdeets[i][23]],
                                'underSymbol': [cdeets[i][24]],
                                'underSecType': [cdeets[i][25]],
                                'marketRuleIds': [cdeets[i][26]],
                                'realExpirationDate': [cdeets[i][27]],
                                'minSize': [cdeets[i][28]],
                                'sizeIncrement': [cdeets[i][29]],
                                'suggestedSizeIncrement': [cdeets[i][30]]
                            })
                        )
                    case _:
                        contract_details_lst.append(
                            pd.DataFrame({cdeets[i]})
                        )
            case 'STK':
                match len(cdeets[i]):
                    case 29:
                        end_of_sec_id_list_ind = 20 + 2 * int(cdeets[i][19])
                        contract_details_lst.append(
                            pd.DataFrame({
                                'symbol': [cdeets[i][0]],
                                'secType': [cdeets[i][1]],
                                'exchange': [cdeets[i][3]],
                                'currency': [cdeets[i][4]],
                                'localSymbol': [cdeets[i][5]],
                                'marketName': [cdeets[i][6]],
                                'tradingClass': [cdeets[i][7]],
                                'conId': [cdeets[i][8]],
                                'minTick': [cdeets[i][9]],
                                'orderTypes': [cdeets[i][10]],
                                'validExchanges': [cdeets[i][11]],
                                'priceMagnifier': [cdeets[i][12]],
                                'longName': [cdeets[i][14]],
                                'primaryExchange': [cdeets[i][15]],
                                'timeZoneId': [cdeets[i][16]],
                                'tradingHours': [cdeets[i][17]],
                                'liquidHours': [cdeets[i][18]],
                                'secIdList': ["{" + ",".join([
                                    "'" +
                                    "':'".join(cdeets[i][x:(x + 2)]) +
                                    "'" for x in range(
                                        20, end_of_sec_id_list_ind, 2
                                    )
                                ]) + "}"],
                                'aggGroup': [
                                    cdeets[i][end_of_sec_id_list_ind]
                                ],
                                'marketRuleIds': [
                                    cdeets[i][end_of_sec_id_list_ind + 1]
                                ],
                                'stockType': [
                                    cdeets[i][end_of_sec_id_list_ind + 2]
                                ],
                                'minSize': [
                                    cdeets[i][end_of_sec_id_list_ind + 3]
                                ],
                                'sizeIncrement': [
                                    cdeets[i][end_of_sec_id_list_ind + 4]
                                ],
                                'suggestedSizeIncrement': [
                                    cdeets[i][end_of_sec_id_list_ind + 5]
                                ]
                            })
                        )
                    case _:
                        end_of_sec_id_list_ind = 23 + 2 * int(cdeets[i][22])
                        contract_details_lst.append(
                            pd.DataFrame({
                                'symbol': [cdeets[i][0]],
                                'secType': [cdeets[i][1]],
                                'exchange': [cdeets[i][3]],
                                'currency': [cdeets[i][4]],
                                'localSymbol': [cdeets[i][5]],
                                'marketName': [cdeets[i][6]],
                                'tradingClass': [cdeets[i][7]],
                                'conId': [cdeets[i][8]],
                                'minTick': [cdeets[i][9]],
                                'orderTypes': [cdeets[i][10]],
                                'validExchanges': [cdeets[i][11]],
                                'priceMagnifier': [cdeets[i][12]],
                                'longName': [cdeets[i][14]],
                                'primaryExchange': [cdeets[i][15]],
                                'industry': [cdeets[i][16]],
                                'category': [cdeets[i][17]],
                                'subcategory': [cdeets[i][18]],
                                'timeZoneId': [cdeets[i][19]],
                                'tradingHours': [cdeets[i][20]],
                                'liquidHours': [cdeets[i][21]],
                                'secIdList': ["{" + ",".join([
                                    "'" + "':'".join(cdeets[i][x:(x + 2)]) + "'"
                                    for
                                    x in range(23, end_of_sec_id_list_ind, 2)
                                ]) + "}"],
                                'aggGroup': [cdeets[i][end_of_sec_id_list_ind]],
                                'marketRuleIds': [
                                    cdeets[i][end_of_sec_id_list_ind + 1]
                                ],
                                'stockType': [
                                    cdeets[i][end_of_sec_id_list_ind + 2]],
                                'minSize': [
                                    cdeets[i][end_of_sec_id_list_ind + 3]],
                                'sizeIncrement': [
                                    cdeets[i][end_of_sec_id_list_ind + 4]
                                ],
                                'suggestedSizeIncrement': [
                                    cdeets[i][end_of_sec_id_list_ind + 5]
                                ]
                            })
                        )
            case "CRYPTO":
                contract_details_lst.append(
                    pd.DataFrame({
                        'symbol': [cdeets[i][0]],
                        'secType': [cdeets[i][1]],
                        'exchange': [cdeets[i][3]],
                        'currency': [cdeets[i][4]],
                        'localSymbol': [cdeets[i][5]],
                        'marketName': [cdeets[i][5]],
                        'tradingClass': [cdeets[i][5]],
                        'conId': [cdeets[i][8]],
                        'minTick': [cdeets[i][9]],
                        'orderTypes': [cdeets[i][10]],
                        'validExchanges': [cdeets[i][11]],
                        'priceMagnifier': [cdeets[i][12]],
                        'longName': [cdeets[i][14]],
                        'timeZoneId': [cdeets[i][15]],
                        'tradingHours': [cdeets[i][16]],
                        'liquidHours': [cdeets[i][17]],
                        'aggGroup': [cdeets[i][18]],
                        'underSymbol': [cdeets[i][19]],
                        'marketRuleIds': [cdeets[i][20]],
                        'minSize': [cdeets[i][21]],
                        'sizeIncrement': [cdeets[i][22]],
                        'suggestedSizeIncrement': [cdeets[i][23]]
                    })
                )
            case _:
                contract_details_lst.append(pd.DataFrame({cdeets}))

    cdeets_df = pd.concat(contract_details_lst, ignore_index=True)

    def hours_str_to_df(hrs_str):
        hrs_str_splt = hrs_str.split(';')

        def format_splt_hrs(splt_hrs):
            hrs_dash_split = splt_hrs.split('-')

            if len(hrs_dash_split) == 1:
                if hrs_dash_split[0].split(":")[1] != 'CLOSED':
                    print("Strange hrs_dash_split string detected:")
                    print(hrs_dash_split)
                    raise NotImplementedError("Unhandled hrs_dash_split")
                return pd.DataFrame(
                    data = {
                        'start_time': None,
                        'end_time': None,
                        'closed': True
                    },
                    index = [
                        datetime.strptime(
                            hrs_dash_split[0].split(":")[0],
                            "%Y%m%d"
                        ).date()
                    ]
                )

            hrs_date = list(set([
                datetime.strptime(
                    x.split(":")[0],'%Y%m%d'
                ).date() for x in hrs_dash_split
            ]))

            if len(hrs_date) != 1:
                try:
                    df = formatter2(hrs_str)
                except Exception as e:
                    warnings.warn("weird hrs_str gave an exception:")
                    print(type(e))
                    print(e)
                    print(f"hrs_str = '{hrs_str}'")


            return pd.DataFrame(
                data = {
                    'start_time': [
                        datetime.strptime(
                            splt_hrs.split("-")[0].split(":")[1],
                            "%H%M"
                        ).time()
                    ],
                    'end_time': [
                        datetime.strptime(
                            splt_hrs.split("-")[1].split(":")[1],
                            "%H%M"
                        ).time()
                    ],
                    'closed': [False]
                },
                index = [hrs_date[0]]
            )

        return pd.concat([format_splt_hrs(x) for x in hrs_str_splt])


    try:
        cdeets_df['liquidHours'] = [
            hours_str_to_df(x) for x in cdeets_df['liquidHours']
        ]
        cdeets_df['tradingHours'] = [
            hours_str_to_df(x) for x in cdeets_df['tradingHours']
        ]
    except IndexError:
        pass

    return cdeets_df
