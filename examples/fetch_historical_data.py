import shinybroker as sb


historical_data = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': "AAPL",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    })
)
print(historical_data['hst_dta'])

# historical Bid/Ask for a Google Call
# the behavior of this one can be spotty if you're running it outside of
#   normal trading hours
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
    durationStr='1 D',
    barSizeSetting='1 hour',
    whatToShow='BID_ASK'
)
print(historical_data_google_bid_ask['hst_dta'])


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

#### Try an example with a bad security definition
#### IBKR considers "SPX" as an index (type="IND"), not a stock.
historical_data_bad_secdef = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': "SPX",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    }),
    barSizeSetting="1 day"
)
print(historical_data_bad_secdef)
