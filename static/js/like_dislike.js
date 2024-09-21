
const likeButton = document.getElementById('like-button');
const dislikeButton = document.getElementById('dislike-button');

likeButton.addEventListener('click', function (event) {
    event.preventDefault(); 
    if (!isUserAuthenticated()) {
        window.location.href = `/login/?next=${encodeURIComponent(window.location.href)}`;
    } else {
        const actionUrl = likeButton.getAttribute('data-action-url');
        sendAjaxRequest(actionUrl, 'like');
    }
});

dislikeButton.addEventListener('click', function (event) {
    event.preventDefault(); 
    if (!isUserAuthenticated()) {
        window.location.href = `/login/?next=${encodeURIComponent(window.location.href)}`;
    } else {
        const actionUrl = dislikeButton.getAttribute('data-action-url');
        sendAjaxRequest(actionUrl, 'dislike');
    }
});

function isUserAuthenticated() {
    return document.body.classList.contains('authenticated'); // Asegúrate de que esta clase esté presente en el cuerpo si el usuario está autenticado
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
                console.log('Error processing the action.');
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

