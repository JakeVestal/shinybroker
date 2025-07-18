from shiny import module, ui, render, reactive

@module.ui
def get_contract_ui(
        label: str = "Increment counter",
        value: str = ""
):
    text_input = ui.input_text(
        id="requested_symbol",
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
        ui.output_data_frame("matching_contracts")
    )

@module.server
def get_contract_server(input, output, session, starting_value):
    count =  reactive.value(0)

    @reactive.effect
    @reactive.event(input.button)
    def get_contract_button_clicked():
        count.set(count() + 1)

    @render.code
    def contract_definition():
        return f"Click count is {count()}"
