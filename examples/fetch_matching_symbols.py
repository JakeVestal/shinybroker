import shinybroker as sb

matching_symbols_aapl = sb.fetch_matching_symbols("AAPL")
print("Stocks matching patterm \"AAPL\":")
print(matching_symbols_aapl['stocks'])
print("Bonds matching patterm \"AAPL\":")
print(matching_symbols_aapl['bonds'])

matching_symbols_goog = sb.fetch_matching_symbols("GOOG")
print("Matching Symbols for \"GOOG\":")
print(matching_symbols_goog)

matching_symbols_no_match = sb.fetch_matching_symbols("string w no matches")
print("If nothing matches, then you get a dictionary of empty data frames:")
print("returned dict:")
print(matching_symbols_no_match)
print("no matching stocks:")
print(matching_symbols_no_match)
print("no matching bonds:")
print(matching_symbols_no_match)
