function update_contractinator_accordion_titles() {
    var titles = [];
    $('#contractinator_accordion .accordion-button').each(
        function() {titles.push($(this).text().trim());});
    Shiny.setInputValue(
        'contractinator_accordion_titles', titles,  {priority: 'event'}
    );
}
