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
        ui.output_ui(
            id=f"{contract_name}_contract_definition"
        ),
        ui.output_ui(
            id=f"{contract_name}_validate_contract_btn"
        ),
        ui.output_ui("contract_verification"),
        text_input,
        ui.input_action_button(
            id=f"{contract_name}_contractinator_smc_btn",
            label="Search for Matching Contracts",
            **{
                "onclick": "Shiny.setInputValue(" +
                           f"'smc_buffer', '{contract_name}');"
            }
        ),
        ui.output_ui("matching_contracts")
    )

def contractinator_ui(contract_names: list | dict):

    if isinstance(contract_names, list):
        contract_names = {x:'' for x in contract_names}

    return ui.accordion(
        *[create_contractinator_panel(k, v) for k, v
          in contract_names.items()],
        id="contractinator_accordion"
    )
