VERSION = '0.6.46'

from importlib.resources import files
from rich import print as rprint
from rich.panel import Panel as rPanel

from re import sub as rsub

rprint(
    rPanel(
        rsub(
            "\\n",
            "",
            files(__package__).joinpath(
                "txt_files", "txt_intro.txt"
            ).read_text(encoding="utf-8")
        ),
        title="ShinyBroker Usage and License",
        subtitle="Read License: https://shinybroker.com/LICENSE.html"
    )
)
print('')

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
from shinybroker.contractinator import contractinator
