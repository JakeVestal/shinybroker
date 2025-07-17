from shiny import module, ui, render, reactive, event
from shiny.express import output, session

@module.ui
def contract_wizard_ui(label: str = "Increment counter"):
    return ui.card(
        ui.card_header("This is " + label),
        ui.input_action_button(id="button", label=label),
        ui.output_code(id="out"),
        ui.input_text(
            id="requested_symbol",
            label="Enter search string:",
            width="400px"
        ).add_style("display:flex;flex-direction:row;align-items: center;")
    )

@module.server
def contract_wizard_server(input, output, session, starting_value):
    count =  reactive.value(starting_value)

    @reactive.effect
    @reactive.event(input.button)
    def _():
        count.set(count() + 1)

    @render.code
    def out():
        return f"Click count is {count()}"
