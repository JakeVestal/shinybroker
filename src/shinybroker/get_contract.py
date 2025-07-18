import pandas as pd

from shiny import module, ui, render, reactive
from shinybroker import fetch_matching_symbols


@module.ui
def get_contract_ui(
        label: str = "Increment counter",
        value: str = ""
):
    text_input = ui.input_text(
        id="search_string",
        label="Enter search string:",
        width="400px",
        value=value
    ).add_style("display:flex;flex-direction:row;align-items:center;")
    text_input.children[0] = text_input.children[0].add_style(
        "width:275px;padding-top:5px;"
    )

    return ui.card(
        ui.card_header(label),
        ui.output_code(id="contract_definition"),
        text_input,
        ui.input_action_button(
            id="button",
            label='Search for Matching Contracts'
        ),
        ui.output_ui("matching_contracts")
    )

@module.server
def get_contract_server(input, output, session, starting_value):

    @render.ui
    @reactive.event(input.button)
    def matching_contracts():
        cm_df = fetch_matching_symbols(input.search_string())
        print(cm_df)

        if cm_df['stocks'].shape[0] == 0:
            if cm_df['bonds'].shape[0] == 0:
                return f"No matches found for: {input.search_string()}"


    # @render.data_frame
    # def matching_contracts():
    #     return render.DataTable(
    #         df(),
    #         width=width,
    #         height=height,
    #         filters=input.filters(),
    #         editable=input.editable(),
    #         selection_mode=input.selection_mode(),
    #     )

    # @render.code
    # def contract_definition():
    #     return f"Click count is {count()}"
