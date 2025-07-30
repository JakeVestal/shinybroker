from shiny import App, ui, reactive, render
from shinywidgets import output_widget
import htmltools



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
    # Provide an id to create a shiny input binding
    ui.accordion(
        *[create_accordion_panel(k,v) for k,v in contract_names.items()],
        id="acc"
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

# Define the UI
# app_ui = ui.page_fluid(
#
# # Include external dependencies: Tailwind CSS and interact.js
# ui.head_content(
#     ui.HTML("""
#     <script src="https://cdn.tailwindcss.com"></script>
#     <script
#      src="https://unpkg.com/interactjs/dist/interact.min.js"></script>
#     """)
# ),
# # Main container for the draggable and resizable card
# ui.div(
#     ui.div(
#         # Card styling with Tailwind CSS, overflow for scroll bars
#         {
#             "id": "contractinator-card",
#             "class": "p-6 bg-white rounded-lg shadow-lg max-w-md" +
#                      "w-full relative",
#             "style": "position: absolute; top: 50px; left: 50px;" +
#                      "overflow: auto; width:450px;"
#         },
#         # Add Contract button
#         ui.input_action_button(
#             "contractinator_add_card_btn",
#             "Add Contract",
#             class_="mb-4 bg-green-500 hover:bg-green-700 text-white" +
#                    "font-bold py-2 px-4 rounded"
#         ),
#         # Container for accordion panels
#         ui.div(
#             {"id": "contractinator-accordion"},
#             # Initial accordion panels
#             ui.HTML(
#                 """
#                 <details id="frog_panel" class="mb-4">
#                     <summary class="font-bold text-lg cursor-pointer
#                     text-blue-600 hover:text-blue-800 flex
#                     justify-between items-center">
#                         <span>Poison Dart Frog</span>
#                         <button
#                         onclick="document.getElementById(
#                         'frog_panel').remove()"
#                         class="text-red-500 hover:text-red-700
#                         font-bold text-sm"
#                         >X</button>
#                     </summary>
#                     <div class="mt-2 p-4 bg-gray-100 rounded">
#                 """
#             ),
#             ui.input_action_button(
#                 "frog_button",
#                 "Say Hello",
#                 **{
#                     "data-panel-title": "Poison Dart Frog",
#                     "onclick": "Shiny.setInputValue(" +
#                                "'panel_title_frog', " +
#                                "this.getAttribute('data-panel-title')" +
#                                ");"
#                 }
#             ).add_class(
#                 class_="mt-2 bg-blue-500 hover:bg-blue-700 " +
#                        "text-white font-bold py-2 px-4 rounded"
#             ),
#             ui.output_text("frog_output").add_class(
#                 class_="mt-2 text-gray-800"
#             ),
#             ui.HTML(
#                 """
#                     </div>
#                 </details>
#                 """
#             )
#         )
#     ),
#     # JavaScript for drag-and-drop, resizing, and dynamic panel addition
#     ui.HTML(
#         """
#         <script>
#             // Drag-and-drop and resizing for the card
#             interact('#contractinator-card')
#                 .draggable({
#                     inertia: true,
#                     autoScroll: true,
#                     modifiers: [
#                         interact.modifiers.restrictRect({
#                             restriction: 'parent',
#                             endOnly: true
#                         })
#                     ],
#                     listeners: {
#                         move: function(event) {
#                             var target = event.target;
#                             var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
#                             var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;
#                             target.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
#                             target.setAttribute('data-x', x);
#                             target.setAttribute('data-y', y);
#                         }
#                     }
#                 })
#                 .resizable({
#                     edges: { left: true, right: true, bottom: true, top: true },
#                     modifiers: [
#                         interact.modifiers.restrictSize({
#                             min: { width: 200, height: 200 }
#                         })
#                     ],
#                     listeners: {
#                         move: function(event) {
#                             var target = event.target;
#                             target.style.width = event.rect.width + 'px';
#                             target.style.height = event.rect.height + 'px';
#                         }
#                     }
#                 });
#
#             // Handle Add Card button click
#             document.getElementById('contractinator_add_card_btn').addEventListener('click', function() {
#                 var panelTitle = prompt('Enter panel name:');
#                 if (panelTitle) {
#                     // Sanitize title to create a valid ID
#                     var panelId = 'panel_' + panelTitle.replace(/[^a-zA-Z0-9]/g, '_') + '_' + Date.now();
#                     var newPanel = document.createElement('details');
#                     newPanel.id = panelId;
#                     newPanel.className = 'mb-4';
#                     newPanel.innerHTML = `
#                         <summary class="font-bold text-lg cursor-pointer text-blue-600 hover:text-blue-800 flex justify-between items-center">
#                             <span>${panelTitle}</span>
#                             <button onclick="document.getElementById('${panelId}').remove()" class="text-red-500 hover:text-red-700 font-bold text-sm">X</button>
#                         </summary>
#                         <div class="mt-2 p-4 bg-gray-100 rounded">
#                             <p>card content</p>
#                             <button id="${panelId}_button" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" data-panel-title="${panelTitle}" onclick="Shiny.setInputValue('${panelId}_title', this.getAttribute('data-panel-title'));">Say Hello</button>
#                             <div id="${panelId}_output" class="mt-2 text-gray-800"></div>
#                         </div>
#                     `;
#                     document.getElementById('contractinator-accordion').appendChild(newPanel);
#                     // Register the new output with Shiny
#                     Shiny.setInputValue('new_panel_output', { id: `${panelId}_output`, title: panelTitle });
#                 }
#             });
#
#             // Handle new panel output registration
#             Shiny.addCustomMessageHandler('register_output', function(message) {
#                 Shiny.bindAll(document.getElementById(message.id));
#             });
#         </script>
#         """
#     ),
#     {"style": "position: relative; min-height: 100vh;"}
# )
#)

# Define the server logic
# def server(input, output, session):
#     # Reactive dictionary to store messages for all panels
#     messages = reactive.Value({})
#
#     # Update message for initial panels
#     @reactive.Effect
#     @reactive.event(input.panel_title_frog)
#     def update_frog_message():
#         panel_title = input.panel_title_frog()
#         messages.set({**messages.get(), "frog_output": f"Hello {panel_title}!"})
#
#
#     # Handle new panel outputs
#     @reactive.Effect
#     @reactive.event(input.new_panel_output)
#     def register_new_output():
#         new_output = input.new_panel_output()
#         output_id = new_output["id"]
#         title = new_output["title"]
#
#         # Register a dynamic output
#         @output
#         @render.text
#         def dynamic_output():
#             return messages.get().get(output_id, "")
#         dynamic_output.__name__ = output_id
#
#
#
#         # Register an effect for the new panel's button
#         @reactive.Effect
#         @reactive.event(lambda: input[f"{output_id.replace('_output', '_title')}"])
#         def update_new_message():
#             panel_title = input[f"{output_id.replace('_output', '_title')}"]()
#             messages.set({**messages.get(), output_id: f"Hello {panel_title}!"})
#
#     # Render text outputs for initial panels
#     @render.text
#     def frog_output():
#         return messages.get().get("frog_output", "")
#
#
# # Create the Shiny app
# app = App(app_ui, server)
# app.run()