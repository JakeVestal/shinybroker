import os

from faicons import icon_svg
from shiny import ui
from shinybroker.contract_samples import contract_samples


def sb_ui(home_ui = ui.p('no ui passed to sb_ui().')):
    return ui.page_sidebar(
        ui.sidebar(
            ui.output_text('next_valid_id_txt'),
            ui.output_text('market_data_type_txt'),
            ui.input_radio_buttons(
                id='market_data_type',
                label='Market Data Type',
                choices={
                    "1": "1: Live",
                    "2": "2: Frozen",
                    "3": "3: Delayed",
                    "4": "4: Delayed Frozen"
                },
                selected="3"
            ),
            ui.output_text("current_time_txt"),
            ui.input_action_button(
                id="req_current_time",
                label="Request Current Time"
            ),
            ui.input_dark_mode(mode="dark"),
        ),
        ui.page_fluid(
            ui.include_css(
                os.path.join(os.path.dirname(__file__), 'www', 'custom.css')
            ),
            ui.include_js(
                os.path.join(
                    os.path.dirname(__file__), 'www',
                    'ib_message_handler.js'
                )
            ),
            ui.navset_pill(
                ui.nav_panel(
                    icon_svg('house'),
                    home_ui
                ),
                # ui.nav_panel(
                #     ui.div(icon_svg('money-bill-transfer'), " Orders"),
                #     ui.h2('Orders')
                # ),
                # ui.nav_panel(
                #     ui.div(icon_svg('money-check-dollar'), " Holdings"),
                #     ui.h2('Holdings')
                # ),
                # ui.nav_panel(
                #     ui.div(icon_svg('satellite-dish'), " Scanner")
                # ),
                ui.nav_panel(
                    ui.div(icon_svg('city'), ' Market Data'),
                    ui.accordion(
                        ui.accordion_panel(
                            'Market Data',
                            ui.a(
                                'IBKR Market Data Documentation',
                                href='https://ibkrcampus.com/ibkr-api-page/' +
                                     'twsapi-doc/#live-md'
                            ),
                            ui.br(),
                            ui.a(
                                'Tick Types',
                                href='https://ibkrcampus.com/ibkr-api-page/' +
                                     'twsapi-doc/#available-tick-types'
                            ),
                            ui.row(
                                ui.column(
                                    5,
                                    ui.input_text_area(
                                        id="md_contract_definition",
                                        label='Contract Definition',
                                        width='450px',
                                        autoresize=True
                                    ),
                                    ui.input_select(
                                        id='md_example_contract',
                                        label='Example Contracts',
                                        choices=dict(zip(
                                            [x + "\ngenericTickList=''\n" +
                                             "snapshot='0'\n" +
                                             "regulatorySnapshot='0'" for x in
                                             contract_samples.keys()],
                                            contract_samples.values()
                                        )),
                                        width='450px'
                                    ),
                                    ui.input_action_button(
                                        id="md_request_market_data_btn",
                                        label="Request Market Data"
                                    )
                                ),
                                ui.column(
                                    7
                                )
                            ),
                            ui.output_text_verbatim("mkt_data_txt")
                        ),
                        ui.accordion_panel(
                            'Historical Data',
                            ui.a(
                                'IBKR Historical Data Documentation',
                                href='https://www.interactivebrokers.com/' +
                                     'campus/ibkr-api-page/twsapi-doc/#hist-md'
                            ),
                            ui.br(),
                            ui.a(
                                'Requesting Historical Bars',
                                href='https://www.interactivebrokers.com/' +
                                     'campus/ibkr-api-page/twsapi-doc/' +
                                     '#cancelling-earliest-data:~:' +
                                     'text=(reqId)-,Historical,-Bars'
                            ),
                            ui.row(
                                ui.column(
                                    5,
                                    ui.input_text_area(
                                        id="hd_contract_definition",
                                        label='Contract Definition',
                                        width='450px',
                                        autoresize=True
                                    ),
                                    ui.input_select(
                                        id='hd_example_contract',
                                        label='Example Contracts',
                                        choices=dict(zip(
                                            [x + "\nendDateTime=''\n" +
                                             "durationStr='1 D'\n" +
                                             "barSizeSetting='1 hour'\n" +
                                             "whatToShow='Trades'\n" +
                                             "useRTH=1\n" +
                                             "formatDate=1\n" +
                                             "keepUpToDate=0" for x in
                                             contract_samples.keys()],
                                            contract_samples.values()
                                        )),
                                        width='450px'
                                    ),
                                    ui.input_action_button(
                                        id="hd_request_market_data_btn",
                                        label="Request Historical Data"
                                    )
                                ),
                                ui.column(
                                    7
                                )
                            ),
                            ui.output_text_verbatim("historical_data_txt")
                        ),
                        open=False,
                        multiple=True
                    )
                ),
                ui.nav_panel(
                    ui.div(icon_svg('eye'), " Inspect"),
                    ui.h2('Interactive Queries'),
                    ui.p(
                        'You can use this section to view the values of the ' +
                        'reactive variables below, but you can also run ' +
                        'queries and explore the results.'
                    ),
                    ui.accordion(
                        ui.accordion_panel(
                            'Matching Symbols',
                            ui.p(
                                'Fetch all symbols at IBKR that ' +
                                'approximately match your search ' +
                                'parameters. Results are separated into ' +
                                '"stocks" and "bonds". "Stocks" includes ' +
                                '"stock-like" contracts such as ETFs.'
                            ),
                            ui.a(
                                'IBKR Documentation',
                                href='https://ibkrcampus.com/ibkr-api-page' +
                                     '/twsapi-doc/#stock-symbol-search'
                            ),
                            ui.row(
                                ui.column(
                                    6,
                                    ui.input_text(
                                        id="requested_symbol",
                                        label="Enter symbol",
                                        value='AAPL'
                                    )
                                ),
                                ui.column(
                                    6,
                                    ui.input_action_button(
                                        id="req_matching_symbols",
                                        label="Request Matching Symbols"
                                    ).add_style('display:block;')
                                )
                            ),
                            ui.input_switch(
                                id="show_matching_stocks",
                                label="Show Matching Stocks",
                                value=False,
                            ).add_style("display:none;"),
                            ui.panel_conditional(
                                "input.show_matching_stocks",
                                ui.h6('Matching Stocks:'),
                                ui.output_data_frame(
                                    "matching_stock_symbols_df"
                                )
                            ),
                            ui.input_switch(
                                id="show_matching_bonds",
                                label="Show Matching Bonds",
                                value=False,
                            ).add_style("display:none;"),
                            ui.panel_conditional(
                                "input.show_matching_bonds",
                                ui.br(),
                                ui.h6('Matching bonds:'),
                                ui.output_data_frame("matching_bond_symbols_df")
                            )
                        ),
                        ui.accordion_panel(
                            'Contract Details',
                            ui.a(
                                'IBKR Contract Class Reference',
                                href='https://ibkrcampus.com/ibkr-api-page/' +
                                     'twsapi-ref/#contract-ref'
                            ),
                            ui.input_text_area(
                                id="cd_contract_definition",
                                label='Contract Definition',
                                width='450px',
                                autoresize=True
                            ),
                            ui.input_select(
                                id='cd_example_contract',
                                label='Example Contracts',
                                width='450px',
                                choices=contract_samples
                            ),
                            ui.input_action_button(
                                id="cd_request_contract_details_btn",
                                label="Request Contract Details"
                            ),
                            ui.output_data_frame("contract_details_df")
                        ),
                        ui.accordion_panel(
                            'Security-Defined Option Parameters',
                            ui.input_text(
                                id="sdop_underlying_symbol",
                                label='Underlying Symbol',
                                value='AAPL',
                            ).add_style('width:125px;display:inline-block;'),
                            ui.input_text(
                                id="sdop_fut_fop_exchange",
                                label="FUT/FOP exchange",
                                value=""
                            ).add_style('width:125px;display:inline-block;'),
                            ui.input_text(
                                id="sdop_underlying_sec_type",
                                label="Underlying Security Type",
                                value="STK"
                            ).add_style('width:125px;display:inline-block;'),
                            ui.input_text(
                                id="sdop_underlying_con_id",
                                label="Underlying Contract ID",
                                value="265598"
                            ).add_style('width:125px;display:inline-block;'),
                            ui.input_action_button(
                                id="req_sec_def_opt_params_btn",
                                label="Request Sec-Def Option Parameters"
                            ).add_style('display:block;'),
                            ui.output_data_frame("sec_def_opt_params_df")
                        ),
                        open=False,
                        multiple=True
                    )
                ),
                ui.nav_panel(
                    ui.div(icon_svg('info'), " Error Messages"),
                    ui.h3('Error Messages'),
                    ui.h5(
                        'Reactive variable: ',
                        ui.code('error_messages()')
                    ),
                    ui.p(
                        'All error messages received during your '
                        'session are stored in ', ui.code('error_messages()'),
                        '. Some error messages will cause alerts to appear ' +
                        'in the webpage as they are received (e.g., "no ' +
                        'matching contracts").'
                    ),
                    ui.p(
                        'Not all "error" messages mean that something went ' +
                        'wrong; for example, those an error id of "-1" are ' +
                        'informative messages about your API connection.'
                    ),
                    ui.output_table("error_messages_df")
                ),
                id="main_tab"
            )
        ),
        title="ShinyBroker: Visual Reactive Trading with IBKR",
        fillable=True,
        class_="bslib-page-dashboard"
    )
