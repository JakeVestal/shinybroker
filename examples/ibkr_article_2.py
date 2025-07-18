import shinybroker as sb
from shiny import Inputs, Outputs, Session, ui

gc_ui = ui.page_fluid(
    sb.get_contract_ui("contract1", "Asset (y-axis)", "MSTR"),
    sb.get_contract_ui("contract2", "Benchmark (x-axis)", "bitcoin")
)

def gc_server_function(
    input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):
    sb.get_contract_server("contract1", starting_value=5)
    sb.get_contract_server("contract2", starting_value=3)

# Create an instance of a ShinyBroker App object using the default ui and server
app = sb.sb_app(
    gc_ui,
    gc_server_function,
    host='127.0.0.1',  # localhost TWS is being served on your local machine
    port=7497,         # make this match the port in your API Settings config
    client_id=10742    # picked at random, choose another Client ID if preferred
)

# Run the app
app.run()