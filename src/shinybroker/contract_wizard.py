from shiny import module, ui, render, reactive, event

@module.ui
def contract_wizard(label: str = "Increment counter"):
    return ui.card(
        ui.card_header("This is " + label),
        ui.input_action_button(id="button", label=label),
        ui.output_code(id="out"),
    )


@module.server
def contract_wizard(input, output, session, starting_value = 0):
    count =  reactive.value(starting_value)

    @reactive.effect
    @reactive.event(input.button)
    def _():
        count.set(count() + 1)

    @render.code
    def out():
        return f"Click count is {count()}"