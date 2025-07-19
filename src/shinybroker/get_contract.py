import pandas as pd

from shiny import module, ui, render, reactive, req
from shinybroker import fetch_matching_symbols, Contract


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
        ui.output_ui("contract_definition"),
        text_input,
        ui.input_action_button(
            id="button",
            label='Search for Matching Contracts'
        ),
        ui.output_ui("matching_contracts")
    )

@module.server
def get_contract_server(input, output, session, starting_value):
    contract_matches = reactive.value(
        {'stocks': pd.DataFrame({}), 'bonds': pd.DataFrame({})}
    )

    @render.ui
    @reactive.event(input.button)
    def matching_contracts():
        cm_df = fetch_matching_symbols(input.search_string())
        contract_matches.set(cm_df)

        if cm_df['stocks'].shape[0] == 0:
            if cm_df['bonds'].shape[0] == 0:
                return f"No matches found for: {input.search_string()}"
            else:
                return ui.output_data_frame("matching_bonds")
        else:
            if cm_df['bonds'].shape[0] == 0:
                return ui.output_data_frame("matching_stocks")
            else:
                return ui.navset_card_tab(
                    ui.nav_panel(
                        "Stocks",
                        ui.output_data_frame("matching_stocks")
                    ),
                    ui.nav_panel(
                        "Bonds",
                        ui.output_data_frame("matching_bonds")
                    )
                )

    @render.data_frame
    def matching_stocks():
        return render.DataTable(
            contract_matches()['stocks'],
            selection_mode="rows"
        )

    @render.data_frame
    def matching_bonds():
        return render.DataTable(
            contract_matches()['bonds'],
            selection_mode="rows"
        )

    selected_contract = reactive.value()

    @reactive.effect
    @reactive.event(matching_stocks.cell_selection)
    def a_stock_row_has_just_been_selected():
        req(len(matching_stocks.cell_selection()['rows']) > 0)
        selected_contract.set(
            Contract(
                contract_matches()['stocks'].iloc[
                    matching_stocks.cell_selection()['rows'][0]
                ]['con_id']
            )
        )

    @reactive.effect
    @reactive.event(matching_bonds.cell_selection)
    def a_bond_row_has_just_been_selected():
        req(len(matching_bonds.cell_selection()['rows']) > 0)
        selected_contract.set(
            Contract(
                contract_matches()['bonds'].iloc[
                    matching_bonds.cell_selection()['rows'][0]
                ]['con_id']
            )
        )


    @render.ui
    @reactive.event(selected_contract)
    def contract_definition():
        return ui.card(
            str(selected_contract()),
            ui.input_action_button(
                "verify_contract_btn",
                "Verify Contract?"
            ),
            ui.input_action_button(
                "accept_contract_btn",
                "Accept Contract"
            )
        )
