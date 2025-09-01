import pandas as pd
import plotly.express as px
import shinybroker as sb
import numpy as np

from datetime import datetime
from faicons import icon_svg
from functools import reduce
from shiny import Inputs, Outputs, Session, ui, reactive, req, render
from shinywidgets import output_widget, render_plotly
from sklearn import linear_model


ui_ = ui.page_fluid(
    ui.row(
        ui.column(
            5,
            sb.contractinator({
                'bitcoin': 'bitcoin',
                'ethereum': 'etherium',
                'litecoin': 'litecoin',
                'bitcoin_cash': 'bitcoin cash',
                'solana': 'solana',
                'cardano': 'cardano',
                'ripple': 'ripple',
                'doge': 'dogecoin',
                'avalanche': 'avalanche',
                'chainlink': 'chainlink',
                'sui': 'sui'
            })
        ),
        ui.column(
            3,
            ui.h4("Tick Parameters"),
            ui.input_text(
                id="duration_string",
                label="Duration String",
                value="5 D"
            ),
            ui.input_text(
                id="bar_size_setting",
                label="Bar Size Setting",
                value="1 hour"
            ),
            ui.input_action_button(
                id="fetch_price_data",
                label="Fetch Price History",
            )
        ),
        ui.column(
            4,
            ui.h5("Retrieved Price History"),
            ui.p(id="price_history_df_caption"),
            ui.output_data_frame("price_history_df_output")
        )
    ),
    ui.row(
        ui.column(
            9,
            ui.h5('Calculated Returns'),
            ui.output_data_frame('historical_log_returns_df_output')
        ),
        ui.column(
            3,
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
    ),
    ui.row(
        ui.column(
            2,
            ui.input_selectize(
                id='x_axis_contract',
                label='X-axis:',
                choices=[],
                multiple=False
            ),
            ui.input_selectize(
                id='y_axis_contract',
                label='Y-axis:',
                choices=[],
                multiple=False
            )
        ),
        ui.column(
            10,
            ui.h5("Benchmark Plot"),
            output_widget("alphabeta_scatter")
        )
    ),
    ui.row(ui.output_ui("alphabeta_trendline_summary"))
)

def server_(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):

    price_history_df = reactive.value(pd.DataFrame({}))
    @render.data_frame
    def price_history_df_output():
        prc_hst = price_history_df().copy()
        req(not prc_hst.empty)
        for col in prc_hst.columns[1:]:
            prc_hst[col] = '$' + prc_hst[col].round(2).apply(lambda x: f"{x:,.2f}")
        prc_hst[prc_hst == "$nan"] = '-'
        return render.DataTable(prc_hst)

    historical_log_returns_df = reactive.value(pd.DataFrame({}))
    @render.data_frame
    def historical_log_returns_df_output():
        hlr_df = historical_log_returns_df().copy()
        req(not hlr_df.empty)
        for col in hlr_df.columns[1:]:
            hlr_df[col] = (hlr_df[col] * 100).round(5).astype(str) + '%'
        return render.DataTable(hlr_df)

    @reactive.effect
    @reactive.event(sb_rvs['contractinator'])
    def updates_x_and_y_axis_selector_choices():
        ctr = sb_rvs['contractinator']()
        req(len(ctr) > 1)
        ui.update_selectize(
            id='x_axis_contract',
            choices=list(ctr.keys()),
            selected=list(ctr.keys())[0]
        )
        ui.update_selectize(
            id='y_axis_contract',
            choices=list(ctr.keys()),
            selected=list(ctr.keys())[1]
        )

    # @render.text
    # def ctr_not_empty():
    #     # This output is used for the JavaScript condition
    #     # Returns "true" if dict is not empty, "false" if empty
    #     print(str(len(sb_rvs['contractinator'].get()) > 0).lower())
    #     return str(len(sb_rvs['contractinator'].get()) > 0).lower()

    @reactive.effect
    @reactive.event(input.fetch_price_data)
    def update_price_history_df():
        req(input.fetch_price_data() > 0)
        if len(sb_rvs['contractinator']()) < 3:
            ui.notification_show(
                "This app requires 3 saved contractinator objects!",
                type="warning"
            )
            req(False)

        historical_price_data = {cname: sb.fetch_historical_data(
            cdef,
            durationStr=input.duration_string(),
            barSizeSetting=input.bar_size_setting()
        ) for cname, cdef in sb_rvs['contractinator']().items()}

        # if any(value is None for value in historical_price_data.values()):
        #     none_values = [key for key, value in historical_price_data.items()
        #                    if value is None]
        #     ui.notification_show(
        #         f"No price data was retrieved for {str(none_values)}. Please "
        #         f"choose a different contract",
        #         duration=None
        #     )
        #     req(False)

        if any(isinstance(value, str) for value in
               historical_price_data.values()):
            str_values = [key for key, value in historical_price_data.items()
                          if isinstance(value, str)]
            for str_val in str_values:
                ui.notification_show(
                    historical_price_data[str_val],
                    duration=None
                )
            req(False)

        def extract_price_data(name, price_data):
            price_df = price_data['hst_dta'][['timestamp', 'close']].copy()
            price_df.rename(columns={'close': name}, inplace=True)
            return price_df

        list_of_price_dfs = [
            extract_price_data(key, value) for key, value in
            zip(historical_price_data.keys(),historical_price_data.values())
        ]

        def merge_list_of_dfs(list_of_dfs):
            return reduce(
                lambda left, right: pd.merge(
                    left, right, on='timestamp', how='outer'
                ),
                list_of_dfs
            )

        prc_hst_df = merge_list_of_dfs(list_of_price_dfs)
        print("Calculated historical log returns:")
        print(prc_hst_df)
        price_history_df.set(prc_hst_df)


    @reactive.effect
    @reactive.event(price_history_df)
    def update_historical_log_returns_df():
        prc_hst = price_history_df()
        req(not prc_hst.empty)
        hlr_df = pd.DataFrame(
            np.log(
                np.array(prc_hst.iloc[1:, 1:]) / np.array(prc_hst.iloc[:-1, 1:])
            )
        )

        hlr_df.insert(loc=0, column='', value=np.array(prc_hst.iloc[1:, 0]))
        hlr_df.columns = prc_hst.columns
        hlr_df['diff'] = prc_hst['timestamp'].diff()[1:].reset_index(drop=True)
        hlr_df = hlr_df[
            hlr_df['diff'] == hlr_df['diff'].value_counts().idxmax()].drop(
            'diff', axis='columns').dropna()
        print("Calculated historical log returns:")
        print(hlr_df)
        historical_log_returns_df.set(pd.DataFrame(hlr_df))


    alpha = reactive.value(float())
    beta = reactive.value(float())

    @reactive.effect
    def update_alpha_beta():
        req(input.x_axis_contract())
        req(input.y_axis_contract())
        hlr_df = historical_log_returns_df().copy()
        req(not hlr_df.empty)

        regr = linear_model.LinearRegression()
        regr.fit(
            hlr_df[input.x_axis_contract()].values.reshape(
                hlr_df.shape[0], 1),
            hlr_df[input.y_axis_contract()].values.reshape(
                hlr_df.shape[0], 1)
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

    @reactive.calc
    def calculate_alphabeta_scatter():
        req(input.x_axis_contract())
        req(input.y_axis_contract())
        hlr_df = historical_log_returns_df().copy()
        req(not hlr_df.empty)

        print(hlr_df)

        fig = px.scatter(
            hlr_df,
            x=input.x_axis_contract(),
            y=input.y_axis_contract(),
            trendline='ols'
        )
        fig.layout.xaxis.tickformat = ',.2%'
        fig.layout.yaxis.tickformat = ',.2%'
        fig.update_layout(plot_bgcolor='white')
        return fig

    @render_plotly
    def alphabeta_scatter():
        return calculate_alphabeta_scatter()

    @render.ui
    def alphabeta_trendline_summary():
        summy = px.get_trendline_results(
            calculate_alphabeta_scatter()
        ).px_fit_results.iloc[0].summary().as_html()
        return ui.div(
            ui.h5("Statsmodels Results"),
            ui.HTML(summy)
        )



# Create an instance of a ShinyBroker App object using the default ui and server
app = sb.sb_app(
    ui_,
    server_,
    host='127.0.0.1',  # localhost TWS is being served on your local machine
    port=7497,         # make this match the port in your API Settings config
    client_id=10742    # picked at random, choose another Client ID if preferred
)

# Run the app
app.run()
