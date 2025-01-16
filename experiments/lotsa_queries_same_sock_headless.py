# creates a sock, pounds it with historical data requests, and then reads them
#   off one by one as they come in


# TWS, before market hours
# IBG, before market hours
# TWS, during market
# IBG, during market

import shinybroker as sb
import time

symbol = "AAPL"
conId = 265598
secType = "STK"
exchange = "SMART"
currency = "USD"
low_strike = .05
high_strike = .05

sec_def_opt_params = sb.fetch_sec_def_opt_params(
    underlyingConId=265598,
    underlyingSymbol="AAPL",
    underlyingSecType="STK"
)
print(sec_def_opt_params)

historical_data = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': "AAPL",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    }),
    durationStr="60 S",
    barSizeSetting="1 min"
)
last_underlying_price = round(historical_data['hst_dta']['close'].iloc[-1])

high_price = last_underlying_price*(1+high_strike)
low_price = last_underlying_price*(1-low_strike)

strikes = [float(x) for x in sec_def_opt_params.loc[
    sec_def_opt_params['exchange'] == exchange, 'strikes'
].iloc[0].split(",") if float(x) >= low_price and float(x) <= high_price]

expiries = [
    x for x in sec_def_opt_params.loc[
        sec_def_opt_params['exchange'] == exchange, 'expirations'
    ].iloc[0].split(",")
]

ib_conn = sb.create_ibkr_socket_conn(client_id=9999)

sleep_time = 0.01
hd_id = 0
hd_ids = []

for strike in strikes:
    for expiry in expiries:
        hd_id += 1
        hd_ids.append(hd_id)
        time.sleep(sleep_time)
        sb.send_ib_message(
            s=ib_conn['ib_socket'],
            msg=sb.req_historical_data(
                reqId=hd_id,
                contract=sb.Contract({
                    'symbol': "AAPL",
                    'secType': "OPT",
                    'exchange': "SMART",
                    'currency': "USD",
                    'lastTradeDateOrContractMonth': expiry,
                    'strike': strike,
                    'right': 'C',
                    'multiplier': '100'
                }),
                durationStr="60 S",
                barSizeSetting="1 min"
            )
        )
        hd_id += 1
        hd_ids.append(hd_id)
        time.sleep(sleep_time)
        sb.send_ib_message(
            s=ib_conn['ib_socket'],
            msg=sb.req_historical_data(
                reqId=hd_id,
                contract=sb.Contract({
                    'symbol': "AAPL",
                    'secType': "OPT",
                    'exchange': "SMART",
                    'currency': "USD",
                    'lastTradeDateOrContractMonth': expiry,
                    'strike': strike,
                    'right': 'C',
                    'multiplier': '100'
                }),
                durationStr="60 S",
                barSizeSetting="1 min"
            )
        )
