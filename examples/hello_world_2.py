import shinybroker as sb
from shiny import Inputs, Outputs, Session, ui, render


# Some UI to add to the app
a_piece_of_new_ui = ui.div(
    ui.input_text(
        id='sb_example_text_in',
        label='Example Input. Type something!'
    ),
    ui.output_code('sb_example_text_out')
)


# Server to support the new UI
# Signature must always contain the following five parameters:
#   input, output, session, ib_socket, and sb_rvs
def a_server_function(
        input: Inputs, output: Outputs, session: Session, ib_socket, sb_rvs
):
    @render.code
    def sb_example_text_out():
        return f"You entered '{input.sb_example_text_in()}'."


# Create a ShinyBroker app with the new ui and server
app = sb.sb_app(
    a_piece_of_new_ui,
    a_server_function,
    host='127.0.0.1',
    port=7497,
    client_id=10742
)

app.run()
