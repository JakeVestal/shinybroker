import shinybroker as sb


apple_deets = sb.fetch_contract_details(
    contract=sb.Contract({
        'symbol': "AAPL",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    })
)
print(apple_deets)

# Contract Details for a Google Call
gc_deets = sb.fetch_contract_details(
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
print(gc_deets)


#### Try an example with a bad security definition
#### IBKR doesn't give historical data for SPX on SMART exchange; you must pass
####   "ARCA" as the exchange to get it to work. If you try the below code,
####   which does not return historical data, you'll get an informative error
####   message suggesting that you check the contract definition.
historical_data_bad_secdef = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': "SPY",
        'secType': "STK",
        'exchange': "ARCA",
        'currency': "USD"
    })
)
print(historical_data_bad_secdef)

#### Try an example with a bad security definition
#### IBKR doesn't give historical data for SPX on SMART exchange; you must pass
####   "ARCA" as the exchange to get it to work. If you try the below code,
####   which does not return historical data, you'll get an informative error
####   message suggesting that you check the contract definition.
historical_data_bad_secdef = sb.fetch_historical_data(
    contract=sb.Contract({
        'symbol': "SPX",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    })
)
print(historical_data_bad_secdef)
