function update_contractinator_accordion_info() {
    let acc_info = [];
    $('#contractinator_accordion .accordion-item').each(function() {
        let name = $(this).find('.accordion-title').first().text().trim();
        let complete = $(this).hasClass('contractinator_completed');
        let contents;
        if (complete) {
            contents = document.getElementById(
                name + "_final_contract").textContent;
        } else {
            contents = document.getElementById(name + "_search_string").value;
        }
        acc_info.push({
            name: name,
            complete: complete,
            contents: contents
        });
    });
    Shiny.setInputValue(
        'contractinator_accordion_info', acc_info, {priority: 'event'}
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
function contractinator_mark_completed(target) {
    const accordionItems = document.querySelectorAll(
        '#contractinator_accordion .accordion-item'
    );
    accordionItems.forEach(item => {
        const dataValue = item.getAttribute('data-value');
        if (dataValue === target) {
            item.classList.add('contractinator_completed');
        }
    })
}