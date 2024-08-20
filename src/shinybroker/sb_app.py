from shiny import Inputs, Outputs, Session, App
from shinybroker.sb_server import sb_server
from shinybroker.sb_ui import sb_ui


def sb_app(
        home_ui=None,
        server_fn=None,
        host='127.0.0.1',
        port=7497,
        client_id=0,
        verbose=False
):
    if home_ui is not None:
        app_ui = sb_ui(home_ui)
    else:
        app_ui = sb_ui()

    def server(input: Inputs, output: Outputs, session: Session):
        ib_socket, sb_rvs = sb_server(
            input=input,
            output=output,
            session=session,
            host=host,
            port=port,
            client_id=client_id,
            verbose=verbose
        )
        if server_fn is not None:
            server_fn(
                input=input,
                output=output,
                session=session,
                ib_socket=ib_socket,
                sb_rvs=sb_rvs
            )

    return App(app_ui, server)
