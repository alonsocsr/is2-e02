document.addEventListener('DOMContentLoaded', function () {
    const shareButton = document.getElementById("share-button");
    const modal = document.getElementById("share-modal");
    const closeButtons = document.querySelectorAll(".modal-close");

    console.log(shareButton); 
    console.log(modal); 
    console.log(closeButtons);

    // muestra el modal cuando "Compartir" es clickeado
    shareButton.addEventListener("click", function() {
        modal.classList.remove("hidden");
    });

    // cierra el modal
    closeButtons.forEach(button => {
        button.addEventListener("click", function() {
            modal.classList.add("hidden");
        });
    });

    // si se hace click fuera del modal se cierra (on blur)
    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.classList.add("hidden");
        }
    });
});