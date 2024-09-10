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
