import pandas as pd
import shinybroker as sb

from shiny import Inputs, Outputs, Session, ui, reactive, req


ui_ = ui.page_fluid(
    # sb.contractinator(['Asset', 'Benchmark1', 'Benchmark2']),
    sb.contractinator({
        'Asset': 'MSTR',
        'Benchmark1': 'SP500',
        'Benchmark2': 'Bitcoin'
    }),
    ui.card(
        ui.card_header("Tick Parameters"),
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
        ),
        style="display:inline-block;",
    )
)

def server_(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):
    @reactive.effect
    @reactive.event(sb_rvs['contractinator'])
    def contractinator_test():
        print(sb_rvs['contractinator']().keys())

    price_history = reactive.value(pd.DataFrame({}))

    @reactive.effect
    @reactive.event(input.fetch_price_data)
    def fetch_price_data():
        print(input.fetch_price_data())
        req(input.fetch_price_data() > 0)
        if len(sb_rvs['contractinator']()) < 3:
            ui.notification_show("Need 3 saved contractinator objects!")

        ph = {cname: sb.fetch_historical_data(
            cdef,
            durationStr=input.duration_string(),
            barSizeSetting=input.bar_size_setting()
        ) for cname, cdef in sb_rvs['contractinator']().items()}

        print(ph)




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
