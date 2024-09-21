document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');
    const ratingValue = document.getElementById('averageRating');
    const userRatingValue = document.getElementById('userRating');
    let currentRating = parseFloat(userRatingValue.textContent) || 0; // Inicializa con el valor existente
    const ratingElement = document.getElementById('rating');
    const contenidoId = ratingElement.getAttribute('data-contenido-id');

    stars.forEach(star => {
        star.addEventListener('click', function () {
            event.preventDefault();
            if (!isUserAuthenticated()) {
                window.location.href = `/login/?next=${encodeURIComponent(window.location.href)}`;
            } else {
                currentRating = this.getAttribute('data-value');
                updateStars(currentRating);
                submitRating(currentRating);
            }
        });

        star.addEventListener('mouseover', function () {
            updateStars(this.getAttribute('data-value'));
        });

        star.addEventListener('mouseleave', function () {
            updateStars(currentRating);
        });
    });
    function isUserAuthenticated() {
        return document.body.classList.contains('authenticated'); // Asegúrate de que esta clase esté presente en el cuerpo si el usuario está autenticado
    }
    function updateStars(rating) {
        stars.forEach(star => {
            if (star.getAttribute('data-value') <= rating) {
                star.setAttribute('fill', '#ec4899');
            } else {
                star.setAttribute('fill', 'currentColor');
            }
        });
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    function submitRating(rating) {
        const formData = new FormData();
        formData.append('puntuacion', rating);

        fetch(`/contenido/${contenidoId}/calificar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar el promedio
                    ratingValue.textContent = data.puntuacion.toFixed(1) + '/5';

                    // Actualizar la puntuación del usuario
                    userRatingValue.textContent = rating;
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    }
});
