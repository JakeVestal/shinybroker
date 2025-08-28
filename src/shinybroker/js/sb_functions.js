function update_contractinator_accordion_titles() {
    var titles = [];
    $('#contractinator_accordion .accordion-button').each(
        function() {titles.push($(this).text().trim());});
    Shiny.setInputValue(
        'contractinator_accordion_titles', titles,  {priority: 'event'}
    );
}
function add_a_contractinator_row(add_row) {
    Shiny.setInputValue(
        'contractinator_row_to_add',
        {value: add_row, call_id: Date.now()},
        {priority:'event'}
    );
}
function rmv_a_contractinator_row(rmv_row) {
    Shiny.setInputValue(
        'contractinator_row_to_rmv',
        {value: rmv_row, call_id: Date.now()},
        {priority:'event'}
    );
}