import pandas as pd
import re
from shiny import module, ui, render, reactive, req, App
from shinybroker import fetch_matching_symbols, Contract, fetch_contract_details


def create_contractinator_panel(contract_name, initial_value):
    text_input = ui.input_text(
        id=f"{contract_name}_search_string",
        label="Enter search string:",
        width="400px",
        value=initial_value
    ).add_style("display:flex;flex-direction:row;align-items:center;")
    text_input.children[0] = text_input.children[0].add_style(
        "width:275px;padding-top:5px;"
    )
    return ui.accordion_panel(
        contract_name,
        text_input,
        ui.input_action_button(
            id=f"{contract_name}_contractinator_smc_btn",
            label="Search for Matching Contracts",
            **{
                "onclick": "Shiny.setInputValue(" +
                           f"'smc_buffer', '{contract_name}');"
            }
        )
    )

def contractinator(contract_names: list | dict = ()):
    # if dict: the keys are accordion panel names, e.g., "Asset",
    #   "Benchmark", and so on, and the values are your initial guess for the
    #   search string.
    #     contract_names = {
    #         'Asset': 'MSTR',
    #         'Benchmark1': 'SP500',
    #         'Benchmark2': 'Bitcoin'
    #     }
    # if list: the keys are just accordion panel names and the initial gueses
    #   is set to ''; i.e., blank.
    #     contract_names = ['Asset', 'Benchmark1', 'Benchmark2']
    # default: empty tuple, just a blank contractinator panel
    #     contract_names = ()

    if not isinstance(contract_names, dict):
        contract_names = {x: '' for x in contract_names}

    return ui.accordion(
        ui.accordion_panel(
            "Contractinator",
            ui.input_text(
                id="new_contractinator_panel_name",
                label="New Contract Name"
            ),
            ui.input_action_button(
                id="add_new_contractinator_panel",
                label="Add New Contract",
            ),
            ui.accordion(
                *[create_contractinator_panel(k, v) for k, v
                  in contract_names.items()],
                id="contractinator_accordion"
            ).add_style("max-height:350px;overflow-y:auto;")
        ),
        id="contractinator_top_container"
    )
