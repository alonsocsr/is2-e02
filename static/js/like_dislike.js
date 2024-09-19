document.addEventListener('DOMContentLoaded', function() {
    const likeButton = document.getElementById('like-button');
    const dislikeButton = document.getElementById('dislike-button');

    likeButton.addEventListener('click', function() {
        const actionUrl = likeButton.getAttribute('data-action-url');
        sendAjaxRequest(actionUrl, 'like');
    });

    dislikeButton.addEventListener('click', function() {
        const actionUrl = dislikeButton.getAttribute('data-action-url');
        sendAjaxRequest(actionUrl, 'dislike');
    });

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
        if (action === 'like') {
            likeButton.querySelector('svg').setAttribute('fill', liked ? '#ec4899' : 'none');
            likeButton.querySelector('svg').setAttribute('stroke', liked ? '#ec4899' : 'currentColor');
            dislikeButton.querySelector('svg').setAttribute('fill', 'none');
            dislikeButton.querySelector('svg').setAttribute('stroke', 'currentColor');
        } else if (action === 'dislike') {
            dislikeButton.querySelector('svg').setAttribute('fill', disliked ? '#ec4899' : 'none');
            dislikeButton.querySelector('svg').setAttribute('stroke', disliked ? '#ec4899' : 'currentColor');
            likeButton.querySelector('svg').setAttribute('fill', 'none');
            likeButton.querySelector('svg').setAttribute('stroke', 'currentColor');
        }
    
        // Actualiza los contadores en el DOM
        document.getElementById('like-count').textContent = likeCount;
        document.getElementById('dislike-count').textContent = dislikeCount;
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});