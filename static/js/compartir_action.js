document.addEventListener("DOMContentLoaded", function () {
  function updateShareCount() {
    // Retrieve the contenido_id from the data attribute
    const contenidoId = document.getElementById("contenido").getAttribute("data-contenido-id");
  
    fetch('/increment-share-count/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: new URLSearchParams({
            'contenido_id': contenidoId  // Use the ID from data attribute
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Share count updated:', data.share_count);
    })
    .catch(error => {
        console.error('Error:', error);
    });
  }
  
  document.getElementById("copy-button").addEventListener("click", function() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(function() {
        alert("Enlace copiado al portapapeles");
        updateShareCount();  // Call function to increment the share count
    });
  });
  
  document.getElementById("facebook-share").addEventListener("click", function() {
    const url = window.location.href;
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
    updateShareCount();  // Increment share count
  });
  
  document.getElementById("x-share").addEventListener("click", function() {
    const url = window.location.href;
    window.open(`https://x.com/intent/tweet?url=${encodeURIComponent(url)}`, '_blank');
    updateShareCount();  // Increment share count
  });
});

