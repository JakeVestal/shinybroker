import shinybroker as sb
from shiny import Inputs, Outputs, Session, ui, render, reactive, req

shdss_ui = ui.page_fluid(
    ui.h2("Historical Data Fetcher"),
    ui.row(
        ui.column(
            3,
            ui.h4('Contract ID'),
            ui.p('The unique `conId` for your security of interest.'),
            ui.input_text(
                id='con_id',
                label='',
                value='265598'
            )
        ),
        ui.column(6),
        ui.column(
            3,
            ui.input_action_button(
                id='fetch_data',
                label='Fetch Historical Data'
            )
        )
    ),
    ui.row(
        ui.column(
            3,
            ui.h6('endDateTime'),
            ui.p('explaination goes here'),
            ui.input_text(id='endDateTime', label='', value='')
        ),
        ui.column(
            3,
            ui.input_text(
                id='durationStr',
                label='durationStr',
                value='1 D'
            )
        ),
        ui.column(
            3,
            ui.input_text(
                id='barSizeSetting',
                label='barSizeSetting',
                value='1 hour'
            )
        ),
        ui.column(
            3,
            ui.input_text(
                id='whatToShow',
                label='whatToShow',
                value='Trades'
            )
        )
    ),
    ui.row(
        ui.column(
            3,
            ui.input_switch(id="useRTH", label="useRTH", value=True)
        ),
        ui.column(
            3,
            ui.input_radio_buttons(
                "formatDate",
                "formatDate",
                {
                    "1": "String Time Zone Date",
                    "2": "Epoch Date",
                    "3": "Day & Time Date"
                }
            )
        ),
        ui.column(
            3,
            ui.input_switch(
                id="keepUpToDate", label="keepUpToDate", value=False
            )
        ),
        ui.column(3)
    ),
    ui.output_ui('hd_selector'),
    ui.output_ui('hd_output')
)


# Server to support the new UI
# Signature must always contain the following five parameters:
#   input, output, session, ib_socket, and sb_rvs
def shdss_server(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):

    @reactive.effect
    @reactive.event(input.fetch_data, ignore_init=True)
    def fetch_historical_data():
        sb.start_historical_data_subscription(
            historical_data=sb_rvs['historical_data'],
            hd_socket=ib_socket,
            contract=sb.Contract({'conId': input.con_id()}),
            endDateTime=input.endDateTime(),
            durationStr=input.durationStr(),
            barSizeSetting=input.barSizeSetting(),
            useRTH=input.useRTH(),
            formatDate=input.formatDate(),
            keepUpToDate=input.keepUpToDate()
        )

    @render.ui
    def hd_selector():
        if len(sb_rvs['historical_data']().keys()) > 0:
            return ui.TagList(
                ui.input_radio_buttons(
                    id='selected_hd_id',
                    label='Select an ID to display historical data',
                    choices=dict(
                        zip(
                            sb_rvs['historical_data']().keys(),
                            sb_rvs['historical_data']().keys()
                        )
                    )
                ),
                ui.output_data_frame('selected_hd_data')
            )
        else:
            return ui.TagList(
                ui.p(
                    'Please make a historical data request and the results ' +
                    'will appear here.'
                )
            )

    @render.data_frame
    def selected_hd_data():
        selected_hd = sb_rvs['historical_data']().get(input.selected_hd_id())
        req('hst_dta' in selected_hd.keys())
        return render.DataTable(selected_hd['hst_dta'])


# Create a ShinyBroker app with the new ui and server
app = sb.sb_app(
    shdss_ui,
    shdss_server,
    host='127.0.0.1',
    port=7497,
    client_id=10742
)

app.run()
