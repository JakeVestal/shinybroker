import pandas as pd
import re

from shiny import module, ui, render, reactive, req
from shinybroker import fetch_matching_symbols, Contract, fetch_contract_details


@module.ui
def contractinator_ui(
        contract_name: str = "",
        starting_search_string: str = ""
):
    text_input = ui.input_text(
        id="search_string",
        label="Enter search string:",
        width="400px",
        value=starting_search_string
    ).add_style("display:flex;flex-direction:row;align-items:center;")
    text_input.children[0] = text_input.children[0].add_style(
        "width:275px;padding-top:5px;"
    )

    return ui.card(
        ui.card_header(contract_name),
        ui.input_text_area(
            id="contract_definition",
            label="Contract Definition",
            width="100%"
        ),
        ui.input_action_button(
            id='validate_contract_btn',
            label="Validate Contract"
        ),
        ui.output_ui("contract_verification"),
        text_input,
        ui.input_action_button(
            id="search_for_matching_contracts_btn",
            label='Search for Matching Contracts'
        ),
        ui.output_ui("matching_contracts")
    )

@module.server
def contractinator_server(input, output, session):

    # namespace of this module as chosen by user
    module_ns = session.ns('contract_definition').split("-")[0]

    # stores contracts found to match the search string
    contract_matches = reactive.value(
        {'stocks': pd.DataFrame({}), 'bonds': pd.DataFrame({})}
    )

    # 1) When search_for_matching_contracts button is clicked,
    #   matching_conracts() runs fetch_matching_symbols() on the search
    #   string and updates the matching_contracts output ui as well as the
    #   contract_matches() reactive variable.
    @render.ui
    @reactive.event(input.search_for_matching_contracts_btn)
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
                        ui.output_data_frame("matching_bonds")
                    )
                )

    # 2) The next two render functions make sure that the datatable the user
    #    is viewing -- stocks or bonds -- is rendered with data from the
    #    reactive variable "contract_matches".
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

    # 3) If the user selects a row in the stocks datatable, create a contract
    #    definition out of that row's data and add it into the
    #    contract_definition text input.
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
        ui.update_text_area('contract_definition', value=cdef_string)

    @reactive.effect
    @reactive.event(input.validate_contract_btn)
    def contract_verification():
        cd = fetch_contract_details(Contract(eval(input.contract_definition())))

        cdeet_tables = ui.HTML(
            cd[[
                "conId", "longName", "symbol", "secType", "subcategory",
                "primaryExchange", "validExchanges", "currency",
                "timeZoneId", "stockType", 'secIdList'
            ]].transpose(copy=True).to_html(
                header=False,
                border=0
            )
        )

        m = ui.modal(
            cdeet_tables,
            title="Accept this contract??",
            size='m',
            easy_close=True,
            footer=ui.div(
                ui.input_action_button("accept_contract","OK"),
                ui.input_action_button(
                    "dont_accept_contract", "Cancel"
                )
            )
        )
        ui.modal_show(m)

