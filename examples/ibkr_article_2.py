import pandas as pd
import pickle
import shinybroker as sb

from functools import reduce
from shiny import Inputs, Outputs, Session, ui, reactive, req, render


ui_ = ui.page_fluid(
    ui.row(
        ui.column(
            5,
            sb.contractinator({
                'Asset': 'MSTR',
                'Benchmark1': 'S&P 500',
                'Benchmark2': 'Bitcoin'
            })
        ),
        ui.column(
            3,
            ui.h4("Tick Parameters"),
            ui.input_text(
                id="duration_string",
                label="Duration String",
                value="1 D"
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
            ui.output_data_frame("price_data_output")
        )
    )
)

def server_(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):

    price_history = reactive.value(pd.DataFrame({}))

    @reactive.effect
    @reactive.event(input.fetch_price_data)
    def fetch_price_data():
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

        if any(value is None for value in historical_price_data.values()):
            none_values = [key for key, value in my_dict.items()
                           if value is None]
            ui.notification_show(
                f"No price data was retrieved for {str(none_values)}. Please "
                f"choose a different contract",
                duration=None
            )

        def extract_price_data(name, price_data):
            price_df = price_data['hst_dta'][['timestamp', 'close']].copy()
            price_df.rename(columns={'close': name}, inplace=True)
            print(f"{price_df.shape[0]} price rows extracted for {name}")
            return price_df

        def merge_stock_dfs(df_list):
            merged_df = reduce(
                lambda left, right: pd.merge(
                    left, right, on='timestamp',
                    how='outer'
                ),
                df_list
            )
            return merged_df

        prc_hst = merge_stock_dfs(
            [extract_price_data(key, value) for key, value in zip(
                historical_price_data.keys(), historical_price_data.values())]
        )

        price_history.set(prc_hst)

    @render.data_frame
    def price_data_output():
        return render.DataTable(
            price_history()
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
