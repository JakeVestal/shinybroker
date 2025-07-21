import pandas as pd
import re

from shiny import module, ui, render, reactive, req
from shinybroker import fetch_matching_symbols, Contract, fetch_contract_details


@module.ui
def contractinator_ui(
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
        ui.input_text_area(
            id="contract_definition",
            label="Contract Definition",
            width="100%"
        ),
        ui.input_action_button(
            'validate_contract',
            "Validate Contract"

        ),
        ui.output_ui("contract_verification"),
        text_input,
        ui.input_action_button(
            id="button",
            label='Search for Matching Contracts'
        ),
        ui.output_ui("matching_contracts")
    )

@module.server
def contractinator_server(input, output, session):

    # contains formatted results from
    contract_matches = reactive.value(
        {'stocks': pd.DataFrame({}), 'bonds': pd.DataFrame({})}
    )

    @render.ui
    @reactive.event(input.button)
    def matching_contracts():
        cm_df = fetch_matching_symbols(input.search_string())

        if cm_df['stocks'].shape[0] == 0:
            if cm_df['bonds'].shape[0] == 0:
                return f"No matches found for: {input.search_string()}"
            else:
                contract_matches.set(cm_df)
                return ui.output_data_frame("matching_bonds")
        else:
            if cm_df['bonds'].shape[0] == 0:
                contract_matches.set(cm_df)
                return ui.output_data_frame("matching_stocks")
            else:
                contract_matches.set(cm_df)
                return ui.navset_card_tab(
                    ui.nav_panel(
                        "Not Bonds",
                        ui.output_data_frame("matching_stocks")
                    ),
                    ui.nav_panel(
                        "Bonds",
                        ui.p(
                            "Your ability to trade and fetch information for " +
                            "bonds depends upon your IBKR " +
                            "trading permissions and data subscriptions."
                        ),
                        ui.output_data_frame("matching_bonds")
                    )
                )

    @render.data_frame
    def matching_stocks():
        return render.DataTable(
            contract_matches()['stocks'],
            selection_mode="row"
        )

    @render.data_frame
    def matching_bonds():
        return render.DataTable(
            contract_matches()['bonds'],
            selection_mode="row"
        )

    selected_contract = reactive.value()

    @reactive.effect
    @reactive.event(matching_stocks.cell_selection)
    def a_stock_row_has_just_been_selected():
        req(len(matching_stocks.cell_selection()['rows']) > 0)
        contract_row = contract_matches()['stocks'].iloc[
            matching_stocks.cell_selection()['rows'][0]
        ]
        sc = Contract({
            'conId': contract_row['con_id'],
            'symbol': contract_row['symbol'],
            'secType': contract_row['sec_type'],
            'exchange': contract_row['primary_exchange'],
            'currency': contract_row['currency'],
            'description': contract_row['description']
        })
        cdef_string = re.sub(r", ", ",\\n", str(sc))
        ui.update_text_area('contract_definition', value =cdef_string)

    @reactive.effect
    @reactive.event(matching_bonds.cell_selection)
    def a_bond_row_has_just_been_selected():
        req(len(matching_bonds.cell_selection()['rows']) > 0)
        contract_row = contract_matches()['bonds'].iloc[
            matching_bonds.cell_selection()['rows'][0]
        ]
        sc = Contract({
            'issuerId': contract_row['issuer_id'],
            'issuer': contract_row['issuer'],
            'exchange': ''
        })
        print('hello')
        idk = str(sc)
        print(idk)
        wut = eval('Contract(idk)')
        print(wut)
        selected_contract.set(sc)


    @render.ui
    @reactive.event(selected_contract)
    def contract_definition():
        print(str(selected_contract()))
        asdf = eval('Contract(str(selected_contract()))')
        print(asdf)
        return ui.card(
            str(selected_contract()),
            ui.input_action_button(
                "verify_contract_btn",
                "Verify Contract?"
            )
        )

    @render.ui
    @reactive.event(input.verify_contract_btn)
    def contract_verification():
        try:
            contract_details = fetch_contract_details(selected_contract())
            print('hello')
            print(contract_details)
        except UserWarning as uw:
            contract_details = "This definition does not match a contract."

        return contract_details
