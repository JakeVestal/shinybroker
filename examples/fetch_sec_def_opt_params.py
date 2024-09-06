import shinybroker as sb

sec_def_opt_params = sb.fetch_sec_def_opt_params(
    underlyingConId=265598,
    underlyingSymbol="AAPL",
    underlyingSecType="STK"
)

print(sec_def_opt_params)
