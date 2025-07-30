import htmltools
# from faicons import icon_svg
from shiny import App, ui, reactive, render
from shinywidgets import output_widget


contract_names = ['Asset', 'Benchmark1', 'Benchmark2']
# contract_names = {'Asset':'MSTR', 'Benchmark1':'SP500', 'Benchmark2':'Bitcoin'}

if isinstance(contract_names, list):
    contract_names = {x:'' for x in contract_names}

def create_accordion_panel(contract_name, initial_value):
    return ui.accordion_panel(
        contract_name,
        ui.input_action_button(
            id=contract_name + "_contractinator_smc_btn",
            label="Search for Matching Contracts",
            **{
                "onclick": "Shiny.setInputValue(" +
                           f"'smc_buffer', '{contract_name}');"
            }
        )
    )

app_ui = ui.page_fluid(
    ui.accordion(
        *[create_accordion_panel(k,v) for k,v
          in contract_names.items()],
        id="contractinator-accordion"
    )
)

def server(input, output, session):
    @reactive.Effect
    @reactive.event(input.smc_buffer)
    def contractinator_get_matching_contracts():
        print(input.smc_buffer())


# Create the Shiny app
app = App(app_ui, server)
app.run()
