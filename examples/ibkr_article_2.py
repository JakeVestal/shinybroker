import shinybroker as sb
from shiny import Inputs, Outputs, Session, ui

ui_ = ui.page_fluid(
    ui.row(
        ui.column(
            4,
            sb.contractinator_ui("contract1", "Asset", "MSTR")
        ),
        ui.column(
            4,
            sb.contractinator_ui("contract2", "Benchmark_1", "bitcoin")
        ),
        ui.column(
            4,
            sb.contractinator_ui("contract3", "Benchmark_2", "SP500")
        )
    )
)

def server_function_(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):
    sb.contractinator_server("contract1")
    sb.contractinator_server("contract2")
    sb.contractinator_server("contract3")

# Create an instance of a ShinyBroker App object using the default ui and server
app = sb.sb_app(
    ui_,
    server_function_,
    host='127.0.0.1',  # localhost TWS is being served on your local machine
    port=7497,         # make this match the port in your API Settings config
    client_id=10742    # picked at random, choose another Client ID if preferred
)

# Run the app
app.run()
