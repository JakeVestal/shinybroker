import pandas as pd


def format_historical_data_input(hst_dta):
    hd_len = len(hst_dta)
    return {
        'startDateStr': hst_dta[1],
        'endDateStr': hst_dta[2],
        'hst_dta': pd.DataFrame({
            'timestamp': [hst_dta[i] for i in range(4, hd_len, 8)],
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
