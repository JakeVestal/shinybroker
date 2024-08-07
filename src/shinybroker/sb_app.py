from shinybroker.sb_ui import sb_ui
from shinybroker.sb_server import sb_server
from shiny import Inputs, Outputs, Session, App, ui


def blank_server(input, outputs, session, ib_socket):
    pass


def sb_app(
        user_ui=ui.div("UI goes here"),
        user_defined_server=blank_server,
        host='127.0.0.1',
        port=7497,
        client_id=0,
        verbose=False
):

    app_ui = sb_ui(user_ui)

    def server(input: Inputs, outputs: Outputs, session: Session):
        ib_socket = sb_server(
            input, outputs, session, host, port, client_id, verbose
        )
        user_defined_server(input, outputs, session, ib_socket)

    return App(app_ui, server)
