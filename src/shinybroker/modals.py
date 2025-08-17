from shiny import ui

def create_sb_modal(content: list, title_txt: str, size='m'):
    return ui.modal(
        content,
        title=ui.div(
            ui.span(title_txt),
            ui.input_action_button("close_modal", "X").add_class(
                "modal_close_button").add_style("margin-right: -15px;"),
            style="display: flex; align-items: center; width: 100%;"
        ),
        size=size,
        footer=None,
        easy_close=False
    )

def sb_upgrade_version_modal(ver, lv):
    return create_sb_modal(
        content = ui.HTML(
            "You are using ShinyBroker Version <strong>" +
            ver +
            "</strong> but Version <strong>" +
            lv +
            "</strong> is available.<br><br>"
            "Because ShinyBroker is under frequent development, it "
            "is highly recommended that you update to the latest "
            "version. To do so, please: <ol>"
            "<li>Stop your ShinyBroker app</li>"
            "<li>Run <code>pip install shinybroker --upgrade</code> "
            "in your terminal</li> "
            "<li> Restart your ShinyBroker app</li>"
            "</ol> Doing so will ensure that you have access to the "
            "latest features and bug fixes."
        ),
        title_txt="Please Update ShinyBroker"
    )

def sb_couldnt_connect_modal(hst, prt, cid):
    return create_sb_modal(
        content = ui.HTML(
            "ShinyBroker tried to connect to an IBKR client on <br>"
            "<br><strong>host</strong>: " + str(hst) + "<br>" +
            "<strong>port</strong>: " + str(prt) + "<br>" +
            "<strong>client_id</strong>: " + str(cid) + "<br>" +
            "<br>...but connection was refused. Please make sure that "
            "an IBKR client such as TWS or IBKG is running and "
            "configured to accept API connections. See the <a href = "
            "'https://shinybroker.com'>ShinyBroker website</a> for "
            "a detailed setup example."
        ),
        title_txt = "Can't connect to IBKR",
    )

sb_insert_new_contractinator_panel_modal = create_sb_modal(
    content = [
        ui.input_action_button(
            id="contractinator_add_a_row",
            label="+"
        ).add_class("plus-button"),
        ui.input_action_button(
            id="contractinator_remove_a_row",
            label=ui.span("-")
        ).add_class("minus-button"),
        ui.span("Add/Remove rows").add_class("vertically_centered"),
        ui.input_action_button(
            id="add_to_contractinator",
            label="Add to Contractinator"
        ),
        ui.output_data_frame("new_contractinator_panels_df_output"),
        ui.p("Double-click to add your contracts to the table above."),
        ui.p("Adding a search string is optional.")
    ],
    title_txt = "Add New Contracts"
)

def sb_contractinator_remove_contracts_modal(contract_titles):
    return create_sb_modal(
        content = [
            ui.input_action_button(
                id="contractinator_remove_selected_contracts",
                label="Remove Selected Contracts"
            ),
            ui.input_checkbox_group(
                id="contractinator_selected_for_removal",
                label="Select Contracts for Removal:",
                choices=contract_titles
            )
        ],
        title_txt = "Remove Contracts"
    )

sb_saves_your_contractinator_modal = create_sb_modal(
    content = [
        ui.help_text(
            "Saves the contracts in your contractinator as a csv"
        ),
        ui.input_text(
            id="save_contractinator_filename",
            label="Choose a filename:",
        ),
        ui.input_file(
            id="save_contractinator_path",
            label="Choose a save location:",
        )
    ],
    title_txt = "Save Contractinator"
)

def sb_contractinator_match_search_modal(mtch_ui, ttxt):
    return create_sb_modal(
        content = [
            ui.output_ui("contractinator_validate_and_add_ui"),
            ui.input_text_area(
                id="contractinator_modal_selected_contract",
                label="Contract Definition:",
                width="100%",
                placeholder="Please select a contract row from the table below"
            ),
            mtch_ui
        ],
        title_txt = ttxt,
        size='xl'
    )
