import shinybroker as sb
from shiny import Inputs, Outputs, Session, reactive


# Declare a server function...
#   ...just like you would when making an ordinary Shiny app.
def step_1_server(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):

    @reactive.effect
    @reactive.event(sb_rvs['connection_info'])
    def make_historical_data_queries():

        # Fetch the hourly trade data for AAPL for the past 3 days.
        sb.start_historical_data_subscription(
            historical_data=sb_rvs['historical_data'],
            hd_socket=ib_socket,
            contract=sb.Contract({
                'symbol': "AAPL",
                'secType': "STK",
                'exchange': "SMART",
                'currency': "USD",
            }),
            durationStr="3 D",
            barSizeSetting="1 hour"
        )

        # Do the same, but for the S&P 500 Index
        sb.start_historical_data_subscription(
            historical_data=sb_rvs['historical_data'],
            hd_socket=ib_socket,
            contract=sb.Contract({
                'symbol': 'SPX',
                'secType': 'IND',
                'currency': 'USD',
                'exchange': 'CBOE'
            }),
            durationStr="3 D",
            barSizeSetting="1 hour"
        )


# create an app object using your server function
# Adjust your connection parameters if not using the default TWS paper trader,
#   or if you want a different client id, etc.
app = sb.sb_app(
    server_fn=step_1_server,
    host='127.0.0.1',
    port=7497,
    client_id=10799,
    verbose=True
)

# run the app.
app.run()
