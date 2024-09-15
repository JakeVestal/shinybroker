import pandas as pd

from datetime import datetime


def format_historical_data_input(hst_dta):
    hd_len = len(hst_dta)
    return {
        'startDateStr': hst_dta[1],
        'endDateStr': hst_dta[2],
        'hst_dta': pd.DataFrame({
            'timestamp': [
                datetime.fromtimestamp(
                    int(hst_dta[i])
                ) for i in range(4, hd_len, 8)
            ],
            'open': [float(hst_dta[i]) for i in range(5, hd_len, 8)],
            'high': [float(hst_dta[i]) for i in range(6, hd_len, 8)],
            'low': [float(hst_dta[i]) for i in range(7, hd_len, 8)],
            'close': [float(hst_dta[i]) for i in range(8, hd_len, 8)],
            'volume': [int(hst_dta[i]) for i in range(9, hd_len, 8)],
            'wap': [
                round(float(hst_dta[i]), 3) for i in range(10, hd_len, 8)
            ],
            'barCount': [int(hst_dta[i]) for i in range(11, hd_len, 8)]
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
