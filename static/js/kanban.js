
document.addEventListener('DOMContentLoaded', function () {
    const columns = document.querySelectorAll('.kanban-column .kanban-items');
    const rejectModal = document.getElementById('rejectModal');
    const confirmModal = document.getElementById('confirmModal');
    const confirmarCambiosBtn = document.getElementById('confirmarCambios');
    const cancelarConfirmacionBtn = document.getElementById('cancelarConfirmacion');
    const guardarRechazoBtn = document.getElementById('guardarRechazo');
    const cancelarRechazoBtn = document.getElementById('cancelarRechazo');

    let cambiosPendientes = [];
    let estadoOriginal = {};

    // Guardar el estado inicial de cada contenido al cargar la página
    function guardarEstadoInicial() {
        document.querySelectorAll('.contenido-item').forEach(draggable => {
            const postId = draggable.getAttribute('data-id');
            const estadoInicial = draggable.closest('.kanban-column').getAttribute('data-status');
            estadoOriginal[postId] = estadoInicial;
        });
    }

    // Verificar si el usuario tiene permiso para mover el contenido
    function tienePermisoMover(post, nuevoEstado) {
        const estadoActual = post.closest('.kanban-column').getAttribute('data-status');
        const esAutor = parseInt(post.getAttribute('data-autor-id')) === usuarioActualId;
        const esModerada = post.getAttribute('data-moderada') === 'true';

        // Restringir movimiento a Edición o Publicación si la categoría no es moderada
        if (estadoActual === 'Borrador' && (nuevoEstado === 'Edicion' || nuevoEstado === 'Publicacion') && esAutor && !esModerada) {
            return false;  // No permitir mover a Edición o Publicación si la categoría no es moderada
        }

        // Lógica para mover si es el autor y la categoría no es moderada
        if (estadoActual === 'Borrador' && nuevoEstado === 'Publicado' && esAutor && !esModerada) {
            return true;  // Mover directamente de Borrador a Publicado si la categoría no es moderada
        }

        return (
            (estadoActual === 'Borrador' && nuevoEstado === 'Edicion' && moverAEditar) ||
            (estadoActual === 'Edicion' && (nuevoEstado === 'Borrador' || nuevoEstado === 'Publicacion') && moverAPublicar) ||
            (estadoActual === 'Publicacion' && (nuevoEstado === 'Edicion' || nuevoEstado === 'Publicado') && moverAPublicado) ||
            (estadoActual === 'Publicado' && nuevoEstado === 'Inactivo' && moverAInactivo) ||
            (estadoActual === 'Inactivo' && nuevoEstado === 'Publicado' && moverAInactivo)
        );
    }

    // Verificar si el usuario actual es el autor del contenido
    function esAutorDelContenido(draggable) {
        const autorId = draggable.getAttribute('data-autor-id');
        return parseInt(autorId) === usuarioActualId;
    }

   // Habilitar el arrastre de las tarjetas
   function setupDraggables() {
    document.querySelectorAll('.contenido-item').forEach(draggable => {
        draggable.addEventListener('dragstart', () => {
            draggable.classList.add('dragging');
        });

        draggable.addEventListener('dragend', () => {
            draggable.classList.remove('dragging');
            const status = draggable.parentElement.closest('.kanban-column').getAttribute('data-status');
            const postId = draggable.getAttribute('data-id');
            const postTitle = draggable.querySelector('h3').textContent;

            // Guardar el cambio pendiente en la lista si fue movido
            const cambioPendiente = cambiosPendientes.find(cambio => cambio.id === postId);
            if (!cambioPendiente || cambioPendiente.status !== status) {
                cambiosPendientes.push({ id: postId, status: status, title: postTitle });
            }

            // Si se mueve de Edición a Borrador o de Publicación a Edición, mostrar modal de rechazo
            const estadoOriginalPost = estadoOriginal[postId];
            if ((estadoOriginalPost === 'Edicion' && status === 'Borrador') ||
                (estadoOriginalPost === 'Publicacion' && status === 'Edicion')) {
                mostrarModalRechazo({ id: postId, title: postTitle });
                
            // Si se mueve a Publicado o a otro estado válido, mostrar modal de confirmación
            } else if (estadoOriginalPost !== status) {
                // Mostrar modal de confirmación
                mostrarModalConfirmacion();   
            }
        });
    });
}

    // Manejo de eventos "dragover" en las columnas
    columns.forEach(column => {
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
            const afterElement = getDragAfterElement(column, e.clientY);
            const dragging = document.querySelector('.dragging');
            const nuevoEstado = column.closest('.kanban-column').getAttribute('data-status');
            const estadoActual = dragging.closest('.kanban-column').getAttribute('data-status');
            
            if (estadoActual === 'Borrador' && !esAutorDelContenido(dragging)) {
                return; 
            }

            if (tienePermisoMover(dragging, nuevoEstado)) {
                if (afterElement == null) {
                    column.appendChild(dragging);
                } else {
                    column.insertBefore(dragging, afterElement);
                }
                dragging.setAttribute('data-status', nuevoEstado);
            }
        });
    });

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.contenido-item:not(.dragging)')];
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    // Sección de rechazo de contenido
    function mostrarModalRechazo(post) {
        document.getElementById('postName').textContent = `Motivo de rechazo para: ${post.title}`;
        postPendienteRechazo = post;
        rejectModal.classList.remove('hidden');
        const rejectForm = document.getElementById('rejectForm');
        rejectForm.action = `/rechazar-contenido/${post.id}`;
    }

    function ocultarModalRechazo() { 
        rejectModal.classList.add('hidden'); 
    }

    guardarRechazoBtn.addEventListener('click', ocultarModalRechazo);

    cancelarRechazoBtn.addEventListener('click', function () {
        ocultarModalRechazo();
        revertirCambios();
    });
    

    // Sección de confirmación de cambios
    function mostrarModalConfirmacion() { confirmModal.classList.remove('hidden'); }
    function ocultarModalConfirmacion() { confirmModal.classList.add('hidden'); }

    confirmarCambiosBtn.addEventListener('click', function () {
        
        confirmarCambiosBtn.disabled = true;
        confirmarCambiosBtn.classList.add('bg-pink-900', 'cursor-not-allowed');
        confirmarCambiosBtn.classList.remove('bg-pink-700');

        fetch(`/update-post-status/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ cambios: cambiosPendientes })
        })
        .then(() => {
            window.location.reload();
        })
        .catch((error) => {
            alert('Error en la conexión o servidor: ' + error.message);
        });
    });

    cancelarConfirmacionBtn.addEventListener('click', function(){
        ocultarModalConfirmacion();
        revertirCambios();
    });

    

    // Revertir los cambios si el usuario cancela la acción
    function revertirCambios () {
        const draggables = document.querySelectorAll('.contenido-item');

        draggables.forEach(draggable => {
            const postId = draggable.getAttribute('data-id');
            const estadoOriginalPost = estadoOriginal[postId];
            const columnaOriginal = document.querySelector(`.kanban-column[data-status="${estadoOriginalPost}"] .kanban-items`);

            columnaOriginal.appendChild(draggable);

            cambiosPendientes = cambiosPendientes.filter(cambio => cambio.id !== postId);
        });
    };

    const mostrarArchivadosBtn = document.getElementById('mostrarArchivados');
    const archivadoModal = document.getElementById('archivadoModal');
    const cerrarArchivadoBtn = document.getElementById('cerrarArchivado');

    mostrarArchivadosBtn.addEventListener('click', () => {
        archivadoModal.classList.remove('hidden');
    });

    cerrarArchivadoBtn.addEventListener('click', () => {
        archivadoModal.classList.add('hidden');
    });
    // Cerrar el modal al hacer clic fuera
    window.addEventListener('click', (e) => {
        if (e.target === archivadoModal) {
            archivadoModal.classList.add('hidden');
        }
    });

    setupDraggables();
    guardarEstadoInicial();

});
