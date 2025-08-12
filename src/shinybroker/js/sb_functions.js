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
