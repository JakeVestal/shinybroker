import shinybroker as sb


# Contract Details for a Stock
apple_deets = sb.fetch_contract_details(
    contract=sb.Contract({
        'symbol': "AAPL",
        'secType': "STK",
        'exchange': "SMART",
        'currency': "USD"
    })
)
print(apple_deets)
#print the hours that AAPL is liquid this week:
print(apple_deets['liquidHours'][0])

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
    })
)
print(gc_deets)


# It's possible to match more than one contract with a call for contract
#   details as in this example which fetches Contract Details for all strikes
#   for Google Calls expiring on '20261218'.
# Note that here, the strike isn't specified, so the contract definition will
#  match more than one contract.
gc_deets_multi = sb.fetch_contract_details(
    contract=sb.Contract({
        'symbol': 'GOOG',
        'secType': 'OPT',
        'exchange': 'SMART',
        'currency': 'USD',
        'lastTradeDateOrContractMonth': '20261218',
        'right': 'C',
        'multiplier': '100'
    })
)
print(gc_deets_multi)


# Try an example with a bad security definition.
# SPX isn't a stock, it's an Index "IND". The call below will return None and
#  print out an informative warning message.
bad_def_details = sb.fetch_contract_details(
    contract=sb.Contract({
        'symbol': "SPX",
        'secType': "STK",
        'exchange': "ARCA",
        'currency': "USD"
    })
)
print(bad_def_details)
