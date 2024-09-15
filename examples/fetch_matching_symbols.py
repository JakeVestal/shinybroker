import shinybroker as sb

matching_symbols_aapl = sb.fetch_matching_symbols("AAPL")
print(matching_symbols_aapl)

matching_symbols_goog = sb.fetch_matching_symbols("GOOG")
print(matching_symbols_goog)

matching_symbols_no_match = sb.fetch_matching_symbols("no symbol match")
print(matching_symbols_no_match)
