document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".star-button").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            let form = this.closest("form");
            let url = form.action;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_interes) {
                    // Actualiza la estrella a rellena (dorado)
                    this.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="star-icon">
                            <path fill="#FF1493" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                        </svg>
                    `;
                } else {
                    // Actualiza la estrella a vacía (gris)
                    this.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="star-icon">
                            <path fill="#b3b3b3" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                        </svg>
                    `;
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
