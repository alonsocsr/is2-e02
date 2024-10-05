
const likeButton = document.getElementById('like-button');
const dislikeButton = document.getElementById('dislike-button');

likeButton.addEventListener('click', function (event) {
    event.preventDefault(); 
    if (!isUserAuthenticated()) {
        showModalLogin('Inicia Sesión', 'Esta función es exclusiva para usuarios autenticados. Si ya tienes una cuenta, inicia sesión. Si no, créala y después hablamos.');
    } else {
        const actionUrl = likeButton.getAttribute('data-action-url');
        sendAjaxRequest(actionUrl, 'like');
    }
});

dislikeButton.addEventListener('click', function (event) {
    event.preventDefault(); 
    if (!isUserAuthenticated()) {
        showModalLogin('Inicia Sesión', 'Esta función es exclusiva para usuarios autenticados. Si ya tienes una cuenta, inicia sesión. Si no, créala y después hablamos.');
    } else {
        const actionUrl = dislikeButton.getAttribute('data-action-url');
        sendAjaxRequest(actionUrl, 'dislike');
    }
});

function isUserAuthenticated() {
    return document.body.classList.contains('authenticated');
}

function sendAjaxRequest(url, action) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ action: action })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateButtonStyles(action, data.liked, data.disliked, data.like_count, data.dislike_count);
            } else {
                console.log('Error en el proceso de la acción.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateButtonStyles(action, liked, disliked, likeCount, dislikeCount) {
    // Actualiza estilos de botones
    likeButton.querySelector('svg').setAttribute('fill', liked ? '#ec4899' : 'currentColor');
    likeButton.querySelector('svg').setAttribute('stroke', liked ? '#ec4899' : 'currentColor');
    dislikeButton.querySelector('svg').setAttribute('fill', disliked ? '#ec4899' : 'currentColor');
    dislikeButton.querySelector('svg').setAttribute('stroke', disliked ? '#ec4899' : 'currentColor');

    // Actualiza contadores
    document.getElementById('like-count').textContent = likeCount;
    document.getElementById('dislike-count').textContent = dislikeCount;
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

