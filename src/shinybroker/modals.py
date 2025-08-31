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

sb_add_rmv_contractinator_panel_modal = create_sb_modal(
    content = [
        ui.div(
            ui.p(
                "Use the table below to add, remove, or edit items. ",
                ui.br(),
                ui.strong("Double-click").add_style("color:#ff007a;"),
                " a cell in the table to edit.",
                ui.br(),
                "Click \"",
                ui.span("Update Contractinator").add_style("color:#d4af37;"),
                "\" when ready."
            ).add_style("flex:1;margin-right:20px;"),
            ui.input_action_button(
                id="update_contractinator",
                label="Update Contractinator"
            ).add_style(
                "display:flex; justify-content:center; align-items:center; "
                "flex: 0 0 auto; margin-bottom: 15px;"
            )
        ).add_style("display:flex; justify-content:space-between;"
                    "align-items:center; width: 100%; padding-right: 75px;"),
        ui.output_data_frame("new_contractinator_panels_df_output"),
        ui.p(
            ui.strong("NOTE"),
            ": All ",
            ui.span("name").add_class("inline-code"),
            " values must start with a letter or underscore and "
            "may contain only letters, digits, hyphens, "
            "or underscores."
        )
    ],
    title_txt = "Add/Remove Contracts",
    size='l'
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
        title_txt = ttxt + ": Match Search",
        size='xl'
    )
