import shinybroker as sb
from shiny import Inputs, Outputs, Session, ui

cw_ui = ui.page_fluid(
    sb.contract_wizard_ui("contract1", "Contract 1"),
    sb.contract_wizard_ui("contract2", "Contract 2")
)

def cw_server_function(
    input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):
    sb.contract_wizard_server("contract1", starting_value=5)
    sb.contract_wizard_server("contract2", starting_value=3)

# Create an instance of a ShinyBroker App object using the default ui and server
app = sb.sb_app(
    cw_ui,
    cw_server_function,
    host='127.0.0.1',  # localhost TWS is being served on your local machine
    port=7497,         # make this match the port in your API Settings config
    client_id=10742    # picked at random, choose another Client ID if preferred
)

# Run the app
app.run()