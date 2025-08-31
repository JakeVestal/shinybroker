import re

import pandas as pd

from shinybroker.ib_fetch_functions import (fetch_matching_symbols,
                                            fetch_contract_details)
from shinybroker.obj_defs import Contract
from shiny import module, ui, render, reactive, req, App


def create_contractinator_panel(initial_panel, initial_value):
    text_input = ui.input_text(
        id=f"{initial_panel}_search_string",
        label="Enter search string:",
        width="400px",
        value=initial_value
    ).add_style("display:flex;flex-direction:row;align-items:center;")
    text_input.children[0] = text_input.children[0].add_style(
        "text-align: right;width: 134px;padding-top: 5px;padding-right:15px;"
        "font-size: 0.85rem;"
    )
    return ui.accordion_panel(
        initial_panel,
        text_input,
        ui.input_action_button(
            id=f"{initial_panel}_contractinator_smc_btn",
            label="Search for Matching Contracts",
            **{
                "onclick": "Shiny.setInputValue("
                           f"'smc_buffer', '{initial_panel}', "
                           "{priority: 'event'});"
            }
        )
    )

def contractinator(
        initial_panels: list | dict = (),
        contractinator_file: str = None,
        contracts: dict = None
):
    """Add a Contractinator to your app

        The Contractinator is a useful tool for working with IBKR contract
        definitions.

        Parameters
        ------------
        initial_panels: list | dict
            Allows you to initialize the contractinator with specified
            panel names, with optional initial guesses for search strings to
            be passed to `fetch_matching_symbols`. Use this if you know what
            variable names you want to assign to your contracts, but you're
            not sure how to create viable `Contract` objects for them. If
            `initial_panels` is a dict; e.g., `{'asset1': 'AAPL'}, then each
            `key` will be assigned to one panel in the contractinator,
            and each `value` will appear as the initial value in the search
            string field for that panel. If `initial_panels` is a list,
            then empty contractinator panels will be created for each element
            and the initial value of the search string field will be left blank.
        contractinator_file: str
            Path, as a string, that indicates the location of a saved
            contractinator file that will be used to populate the
            contractinator when it is created.
        contracts: dict
            A Python dictionary in which each `key` contains the name of a
            contractinator panel and each `value` contains a contract
            definition. Used to populate the contractinator when it is created.

        Examples
        --------
        ```
        {{< include ../examples/fetch_sec_def_opt_params.py >}}
        ```
        """

    if not isinstance(initial_panels, dict):
        initial_panels = {x: '' for x in initial_panels}

    initial_contractinator_items = ui.accordion(
        *[create_contractinator_panel(k, v) for k, v
          in initial_panels.items()],
        id="contractinator_accordion"
    )

    return ui.div(
        ui.accordion(
            ui.accordion_panel(
                "Contractinator",
                ui.input_action_button(
                    id="add_rmv_contractinator_panels",
                    label="Add/Remove Contracts",
                    onclick="update_contractinator_accordion_info()"
                ).add_style("width:200px;"),
                initial_contractinator_items
            ),
            id="contractinator_top_container"
        )
    )
