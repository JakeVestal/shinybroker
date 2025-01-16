import shinybroker as sb
import time
from shiny import Inputs, Outputs, Session, reactive, ui

app_ui = ui.div(ui.input_action_button(id='go', label='Go'))

# Declare a server function...
#   ...just like you would when making an ordinary Shiny app.
def step_1_server(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):

    @reactive.effect
    @reactive.event(input.go, ignore_init=True)
    def make_historical_data_queries():

        symbol = "AAPL"
        conId = 265598
        secType = "STK"
        exchange = "SMART"
        currency = "USD"
        low_strike = .05
        high_strike = .05

        sec_def_opt_params = sb.fetch_sec_def_opt_params(
            underlyingConId=conId,
            underlyingSymbol=symbol,
            underlyingSecType=secType
        )

        historical_data = sb.fetch_historical_data(
            contract=sb.Contract({
                'symbol': symbol,
                'secType': secType,
                'exchange': exchange,
                'currency': currency
            }),
            durationStr="60 S",
            barSizeSetting="1 min"
        )

        last_underlying_price = round(
            historical_data['hst_dta']['close'].iloc[-1]
        )

        high_price = last_underlying_price * (1 + high_strike)
        low_price = last_underlying_price * (1 - low_strike)

        strikes = [float(x) for x in sec_def_opt_params.loc[
            sec_def_opt_params['exchange'] == exchange, 'strikes'
        ].iloc[0].split(",") if low_price <= float(x) <= high_price]

        expiries = [
            x for x in sec_def_opt_params.loc[
                sec_def_opt_params['exchange'] == exchange, 'expirations'
            ].iloc[0].split(",")
        ]

        sleep_time = 0.01
        hd_id = 0

        for strike in strikes:
            for expiry in expiries:
                hd_id += 1
                print(str(hd_id) + ", P" + str(strike) + ", " + str(expiry))
                time.sleep(sleep_time)
                sb.start_historical_data_subscription(
                    historical_data=sb_rvs['historical_data'],
                    hd_socket=ib_socket,
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
                hd_id += 1
                print(str(hd_id) + ", P: " + str(strike) + ", " + str(expiry))
                time.sleep(sleep_time)
                sb.start_historical_data_subscription(
                    historical_data=sb_rvs['historical_data'],
                    hd_socket=ib_socket,
                    contract=sb.Contract({
                        'symbol': "AAPL",
                        'secType': "OPT",
                        'exchange': "SMART",
                        'currency': "USD",
                        'lastTradeDateOrContractMonth': expiry,
                        'strike': strike,
                        'right': 'P',
                        'multiplier': '100'
                    }),
                    durationStr="60 S",
                    barSizeSetting="1 min"
                )


# create an app object using your server function
# Adjust your connection parameters if not using the default TWS paper trader,
#   or if you want a different client id, etc.
app = sb.sb_app(
    home_ui=app_ui,
    server_fn=step_1_server,
    host='127.0.0.1',
    port=7497,
    client_id=10799,
    verbose=True
)

# run the app.
app.run()
