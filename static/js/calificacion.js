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
                showModalLogin('Inicia Sesión', 'Esta función es exclusiva para usuarios autenticados. Si ya tienes una cuenta, inicia sesión. Si no, créala y después hablamos.');
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
    function showModalLogin(title, message) {
        const modalLogin = document.getElementById('modalLogin');
        if (modalLogin) {
            modalLogin.classList.remove('hidden');
            document.getElementById('closeButton').classList.remove('hidden');  // Mostrar el botón de cerrar
            document.getElementById('modal-title').textContent = title;
            document.getElementById('modal-message').textContent = message;
            
            
        }
    }
});
