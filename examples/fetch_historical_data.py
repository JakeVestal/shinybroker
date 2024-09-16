import shinybroker as sb


historical_data = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': "AAPL",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    })
)
print(historical_data)


# historical Bid/Ask for a Google Call
historical_data_google_bid_ask = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': 'GOOG',
        'secType': 'OPT',
        'exchange': 'SMART',
        'currency': 'USD',
        'lastTradeDateOrContractMonth': '20261218',
        'strike': 160,
        'right': 'C',
        'multiplier': '100'
    }),
    durationStr='1 W',
    barSizeSetting='1 day',
    whatToShow='BID_ASK'
)
print(historical_data_google_bid_ask)


#### Try an example with a bad barSizeSetting
#### fetch_historical_data prints an informative error message and returns None
historical_data_bad_barsize = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': "AAPL",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    }),
    barSizeSetting="1 hrs"
)
print(historical_data_bad_barsize)
