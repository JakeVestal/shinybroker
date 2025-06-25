VERSION = '0.6.35'

from rich import print as rprint
from rich.panel import Panel as rPanel
rprint(
    rPanel(
        "ShinyBroker is an ongoing project that is developed and maintained "
        "by the FinTech Master's Program at Duke University and is freely "
        "available to the public for use on paper trading accounts." ,
        title="Welcome to ShinyBroker",
        subtitle="https://shinybroker.com"
    )
)

from shinybroker.connection import (
    create_ibkr_socket_conn,
    read_ib_msg,
    send_ib_message
)
from shinybroker.format_ibkr_inputs import *
from shinybroker.market_data_subscriptions import (
    start_mkt_data_subscription,
    start_historical_data_subscription
)
from shinybroker.msgs_to_ibkr import *
from shinybroker.obj_defs import Contract, ComboLeg, DeltaNeutralContract
from shinybroker.sb_app import sb_app
from shinybroker.ib_fetch_functions import *
