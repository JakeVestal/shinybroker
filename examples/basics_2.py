import numpy as np
import pandas as pd
import shinybroker as sb

from datetime import datetime
from faicons import icon_svg
from sklearn import linear_model
from shiny import Inputs, Outputs, Session, reactive, ui, req, render

a_ui_obj = ui.page_fluid(
    ui.row(
        ui.h5('Calculated Returns'),
        ui.column(
            7,
            ui.output_data_frame('log_returns_df')
        ),
        ui.column(
            5,
            ui.value_box(
                title="Alpha",
                value=ui.output_ui('alpha_txt'),
                showcase=icon_svg('chart-line')
            ),
            ui.value_box(
                title="Beta",
                value=ui.output_ui('beta_txt'),
                showcase=icon_svg('chart-line')
            )
        )
    )
)

# Declare a server function...
#   ...just like you would when making an ordinary Shiny app.
def a_server_function(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):
    # Only set this variable once. Reactive functions that depend upon it will
    #   run when the app is initialized, after the socket has been connected
    #   and properly set up by ShinyBroker.
    run_once = reactive.value(True)

    @reactive.effect
    @reactive.event(run_once)
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
            barSizeSetting="1 hour",
            formatDate=2
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
            barSizeSetting="1 hour",
            formatDate=2
        )

    @reactive.calc
    def calculate_log_returns():
        hd = sb_rvs['historical_data']()

        # Make sure that BOTH assets have been added to historical_data
        try:
            hd['2']['hst_dta'].loc[1:, 'close']
        except KeyError:
            req('')

        asset_1 = pd.DataFrame({
            'timestamp': [
                datetime.fromtimestamp(int(x)) for
                x in hd['1']['hst_dta'].loc[1:, 'timestamp']
            ],
            'aapl_returns': np.log(
                hd['1']['hst_dta'].loc[1:, 'close'].reset_index(drop=True) /
                hd['1']['hst_dta'].iloc[:-1]['close'].reset_index(drop=True)
            )
        })
        asset_2 = pd.DataFrame({
            'timestamp': [
                datetime.fromtimestamp(int(x)) for
                x in hd['2']['hst_dta'].loc[1:, 'timestamp']
            ],
            'spx_returns': np.log(
                hd['2']['hst_dta'].loc[1:, 'close'].reset_index(drop=True) /
                hd['2']['hst_dta'].iloc[:-1]['close'].reset_index(drop=True)
            )
        })
        return pd.merge(asset_1, asset_2, on='timestamp', how='inner')

    @render.data_frame
    def log_returns_df():
        return render.DataTable(calculate_log_returns())

    alpha = reactive.value()
    beta = reactive.value()

    @reactive.effect
    def update_alpha_beta():
        log_rtns = calculate_log_returns()
        regr = linear_model.LinearRegression()
        regr.fit(
            log_rtns.spx_returns.values.reshape(log_rtns.shape[0], 1),
            log_rtns.aapl_returns.values.reshape(log_rtns.shape[0], 1)
        )
        alpha.set(regr.intercept_[0])
        beta.set(regr.coef_[0][0])

    @render.text
    def alpha_txt():
        return f"{alpha() * 100:.7f} %"

    @render.text
    def beta_txt():
        return str(round(beta(), 3))


# create an app object using your server function
# Adjust your connection parameters if not using the default TWS paper trader,
#   or if you want a different client id, etc.
app = sb.sb_app(
    home_ui=a_ui_obj,
    server_fn=a_server_function,
    host='127.0.0.1',
    port=7497,
    client_id=10742,
    verbose=True
)

# run the app.
app.run()