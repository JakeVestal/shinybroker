import numpy as np
import pandas as pd
import shinybroker as sb

from datetime import datetime
from faicons import icon_svg
from sklearn import linear_model
from shiny import Inputs, Outputs, Session, reactive, ui, req, render
from shiny.types import SilentException

step_2_ui = ui.page_fluid(
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
def step_2_server(
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
            aapl_rtns = hd['1']['hst_dta']
            spx_rtns  = hd['2']['hst_dta']
        except KeyError:
            return None

        asset_1 = pd.DataFrame({
            'timestamp': [
                datetime.fromtimestamp(int(x)) for
                x in hd['1']['hst_dta'].loc[1:, 'timestamp']
            ],
            'aapl_returns': np.log(
                aapl_rtns.loc[1:, 'close'].reset_index(drop=True) /
                aapl_rtns.iloc[:-1]['close'].reset_index(drop=True)
            )
        })
        asset_2 = pd.DataFrame({
            'timestamp': [
                datetime.fromtimestamp(int(x)) for
                x in hd['2']['hst_dta'].loc[1:, 'timestamp']
            ],
            'spx_returns': np.log(
                spx_rtns.loc[1:, 'close'].reset_index(drop=True) /
                spx_rtns.iloc[:-1]['close'].reset_index(drop=True)
            )
        })
        return pd.merge(asset_1, asset_2, on='timestamp', how='inner')

    @render.data_frame
    def log_returns_df():
        if calculate_log_returns() is None:
            raise SilentException()
        return render.DataTable(calculate_log_returns())

    alpha = reactive.value(float())
    beta = reactive.value(float())

    @reactive.effect
    def update_alpha_beta():
        log_rtns = calculate_log_returns()

        if log_rtns is None:
            raise SilentException()

        regr = linear_model.LinearRegression()
        regr.fit(
            log_rtns.spx_returns.values.reshape(log_rtns.shape[0], 1),
            log_rtns.aapl_returns.values.reshape(log_rtns.shape[0], 1)
        )
        alpha.set(regr.intercept_[0])
        beta.set(regr.coef_[0][0])

    @render.text
    def alpha_txt():
        a = req(alpha())
        return f"{a * 100:.7f} %"

    @render.text
    def beta_txt():
        b = req(beta())
        return str(round(b, 3))


# create an app object using your server function
# Adjust your connection parameters if not using the default TWS paper trader,
#   or if you want a different client id, etc.
app = sb.sb_app(
    home_ui=step_2_ui,
    server_fn=step_2_server,
    host='127.0.0.1',
    port=7497,
    client_id=10799,
    verbose=True
)

# run the app.
app.run()
