import shinybroker as sb
from shiny import Inputs, Outputs, Session, reactive, render, ui, App, module
import os


IB_HOST = '127.0.0.1'
IB_PORT = 7497
IB_CLIENT_ID = 10645

app_ui = sb.sb_ui()


def server(input: Inputs, output: Outputs, session: Session):
    exec(sb.sb_server_code)


app = App(app_ui, sb.sb_server)

app.run()
