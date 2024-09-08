document.addEventListener('DOMContentLoaded', function () {
    const dropdownButton = document.getElementById('categoryDropdown');
    const dropdownMenu = document.getElementById('categoryMenu');

    dropdownButton.addEventListener('click', function () {
        dropdownMenu.classList.toggle('hidden');
    });

    // Cierra el dropdown si se hace clic fuera de él
    document.addEventListener('click', function (event) {
        const isClickInside = dropdownButton.contains(event.target) || dropdownMenu.contains(event.target);
        if (!isClickInside) {
            dropdownMenu.classList.add('hidden');
        }
    });document.addEventListener('DOMContentLoaded', function () {
        const dropdownButton = document.getElementById('categoryDropdown');
        const dropdownMenu = document.getElementById('categoryMenu');
    
        if (dropdownButton && dropdownMenu) {
            dropdownButton.addEventListener('click', function () {
                dropdownMenu.classList.toggle('hidden');
            });
    
            document.addEventListener('click', function (event) {
                const isClickInside = dropdownButton.contains(event.target) || dropdownMenu.contains(event.target);
                if (!isClickInside) {
                    dropdownMenu.classList.add('hidden');
                }
            });
        } else {
            console.error('Dropdown button or menu not found.');
        }
    });
});