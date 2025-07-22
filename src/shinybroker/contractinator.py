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
            id='validate_contract_btn',
            label="Validate Contract"
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

