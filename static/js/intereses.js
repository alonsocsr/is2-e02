const categoryButtons = document.querySelectorAll('.circle-button');

categoryButtons.forEach(button => {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        if (!isUserAuthenticated()) {
            showModalLogin('Inicia Sesión', 'Esta función es exclusiva para usuarios autenticados. Si ya tienes una cuenta, inicia sesión. Si no, créala y después hablamos.');
        } else {
            const actionUrl = button.getAttribute('data-action-url');
            sendAjaxRequest(actionUrl, button);
        }
    });
});

function isUserAuthenticated() {
    return document.body.classList.contains('authenticated');
}

function sendAjaxRequest(url, button) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateButtonStyles(button, data.is_interes);
            } else {
                console.log('Error en el proceso de la acción.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateButtonStyles(button, is_interes) {
    if (is_interes) {
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#ec4899" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
        `;
        button.setAttribute('title', 'Eliminar de favoritos');
    } else {
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#6b7280" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
        `;
        button.setAttribute('title', 'Agregar a favoritos');
    }
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function showModalLogin(title, message) {
    const modalLogin = document.getElementById('modalLogin');
    if (modalLogin) {
        modalLogin.classList.remove('hidden');
        document.getElementById('closeButton').classList.remove('hidden');  // Mostrar el botón de cerrar
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-message').textContent = message;
        
        
    }
}