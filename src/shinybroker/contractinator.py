import pandas as pd
import re
from shiny import module, ui, render, reactive, req, App
from shinybroker import fetch_matching_symbols, Contract, fetch_contract_details


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
        contractinator_file: str | None = None,
        contracts: dict = None
):
    # if dict: the keys are accordion panel names, e.g., "Asset",
    #   "Benchmark", and so on, and the values are your initial guess for the
    #   search string.
    #     initial_panels = {
    #         'Asset': 'MSTR',
    #         'Benchmark1': 'SP500',
    #         'Benchmark2': 'Bitcoin'
    #     }
    # if list: the keys are just accordion panel names and the initial gueses
    #   is set to ''; i.e., blank.
    #     initial_panels = ['Asset', 'Benchmark1', 'Benchmark2']
    # default: empty tuple, just a blank contractinator panel
    #     initial_panels = ()

    if not isinstance(initial_panels, dict):
        initial_panels = {x: '' for x in initial_panels}

    initial_contractinator_items = ui.accordion(
        *[create_contractinator_panel(k, v) for k, v
          in initial_panels.items()],
        id="contractinator_accordion"
    )

    return ui.accordion(
        ui.accordion_panel(
            "Contractinator",
            ui.input_action_button(
                id="add_new_contractinator_panel",
                label="Add New Contract",
            ),
            initial_contractinator_items
        ),
        id="contractinator_top_container"
    )
