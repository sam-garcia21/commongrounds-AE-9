
window.addEventListener('DOMContentLoaded', (event) => {
    const addMoreBtn = document.getElementById('add-more');
    const removeBtns = document.querySelectorAll('.remove-button');
    const totalForms = document.getElementById('id_job-form-TOTAL_FORMS');

    addMoreBtn.addEventListener('click', () => {
        const currentFormCount = parseInt(totalForms.value);
        const container = document.getElementById('create-list');
        const template = document.getElementById('empty-form').innerHTML;

        const newFormHtml = template.replace(/__prefix__/g, currentFormCount);
        
        container.insertAdjacentHTML('beforeend', newFormHtml);
        const updatedContainer = document.getElementById('create-list');

        const newFormRow = updatedContainer.lastElementChild;
        const removeBtn = newFormRow.querySelector('.remove-button');
        removeBtn.addEventListener('click', () => {
            const formRow = newFormRow; 
            const deleteCheckbox = formRow.querySelector('input[name$="-DELETE"]');
            deleteCheckbox.checked = true; 
            formRow.style.display = 'none'; 
        });
        
        totalForms.setAttribute('value', currentFormCount + 1);
    });

    removeBtns.forEach(button => {
        button.addEventListener('click', () => {
            const formRow = button.parentElement; 
            const deleteCheckbox = formRow.querySelector('input[name$="-DELETE"]');
            deleteCheckbox.checked = true; 
            formRow.style.display = 'none';
        });
    })
});