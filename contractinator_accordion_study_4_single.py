import pandas as pd
import re
from shiny import module, ui, render, reactive, req, App
from shinybroker import fetch_matching_symbols, Contract, fetch_contract_details


# contract_names = ['Asset', 'Benchmark1', 'Benchmark2']
contract_names = {'Asset':'MSTR', 'Benchmark1':'SP500', 'Benchmark2':'Bitcoin'}

if isinstance(contract_names, list):
    contract_names = {x:'' for x in contract_names}

def create_accordion_panel(contract_name, initial_value):
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


app_ui = ui.page_fluid(
    ui.accordion(
        *[create_accordion_panel(k,v) for k,v
          in contract_names.items()],
        id="contractinator_accordion"
    )
)

def server(input, output, session):

    # stores contracts found to match the search string
    contract_matches = reactive.value(
        {'stocks': pd.DataFrame({}), 'bonds': pd.DataFrame({})}
    )

    # 1) When a search_for_matching_contracts button is clicked,
    #   matching_conracts() runs fetch_matching_symbols() on the search
    #   string and updates the matching_contracts output ui as well as the
    #   contract_matches() reactive variable.
    @reactive.Effect
    @reactive.event(input.smc_buffer)
    def contractinator_get_matching_contracts():
        cm_df = fetch_matching_symbols(input.search_string())
        print(cm_df)


# Create the Shiny app
app = App(app_ui, server)
app.run()
