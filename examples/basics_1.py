import select
import shinybroker as sb
from shiny import Inputs, Outputs, Session


# Declare a server function...
#   ...just like you would when making an ordinary Shiny app.
def a_server_function(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):

    # use select to wait for the socket to be ready for writing
    (rd, wt, er) = select.select([], [ib_socket], [])
    # when it's ready, send a request for historical data, hourly, for Apple,
    #   over the past 3 days
    wt[0].send(
        sb.req_historical_data(
            reqId=1,
            contract=sb.Contract({
                'symbol': "AAPL",
                'secType': "STK",
                'exchange': "SMART",
                'currency': "USD",
            }),
            durationStr="3 D",
            barSizeSetting="1 hour"
        )
    )

    # Do the same, but for the S&P 500 Index
    (rd, wt, er) = select.select([], [ib_socket], [])
    wt[0].send(
        sb.req_historical_data(
            reqId=1,
            contract=sb.Contract({
                'symbol': 'SPX',
                'secType': 'IND',
                'currency': 'USD',
                'exchange': 'CBOE'
            }),
            durationStr="3 D",
            barSizeSetting="1 hour"
        )
    )

# create an app object using your server function
app = sb.sb_app(
    server_fn=a_server_function,
    host='127.0.0.1',
    port=7497,
    client_id=10742,
    verbose=True
)

# run the app.
app.run()
