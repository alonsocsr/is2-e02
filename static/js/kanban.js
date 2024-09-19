
document.addEventListener('DOMContentLoaded', function () {
    const columns = document.querySelectorAll('.kanban-column .kanban-items');
    const guardarBtn = document.getElementById('guardarCambios');
    const revertirBtn = document.getElementById('revertirCambios');
    const rejectModal = document.getElementById('rejectModal');
    const confirmModal = document.getElementById('confirmModal');
    const guardarRechazoBtn = document.getElementById('guardarRechazo');
    const confirmarCambiosBtn = document.getElementById('confirmarCambios');
    const cancelarRechazoBtn = document.getElementById('cancelarRechazo');
    const cancelarConfirmacionBtn = document.getElementById('cancelarConfirmacion');

    let cambiosPendientes = [];
    let estadoOriginal = {};
    let rechazosPendientes = [];

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

            // Si se mueve de Edición a Borrador o de Publicación a Edición, requerir motivo de rechazo
            const estadoOriginalPost = estadoOriginal[postId];
            if ((estadoOriginalPost === 'Edicion' && status === 'Borrador') ||
                (estadoOriginalPost === 'Publicacion' && status === 'Edicion')) {
                rechazosPendientes.push({ id: postId, title: postTitle });
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

    // Al hacer clic en guardar cambios
    guardarBtn.addEventListener('click', function () {
        if (rechazosPendientes.length > 0) {
            // Si hay rechazos pendientes, mostrar el modal de rechazo para el primer post
            mostrarModalRechazo(rechazosPendientes[0]);
        } else {
            // Si no hay rechazos pendientes, mostrar el modal de confirmación
            mostrarModalConfirmacion();
        }
    });

    // Mostrar modal de rechazo si hay movimientos que lo requieren
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

    // Guardar el motivo de rechazo
    guardarRechazoBtn.addEventListener('click', function () {
        // Si quedan más rechazos pendientes, mostrar el siguiente modal
        if (rechazosPendientes.length > 0) {
            mostrarModalRechazo(rechazosPendientes[0]);
        } else {
            ocultarModalRechazo();
            mostrarModalConfirmacion();
        }
    });
    
    confirmarCambiosBtn.addEventListener('click', function () {
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


    cancelarRechazoBtn.addEventListener('click', ocultarModalRechazo);
    cancelarConfirmacionBtn.addEventListener('click', ocultarModalConfirmacion);

    function mostrarModalConfirmacion() { confirmModal.classList.remove('hidden'); }
    function ocultarModalConfirmacion() { confirmModal.classList.add('hidden'); }

    // Función para revertir los cambios
    revertirBtn.addEventListener('click', function () {
        const draggables = document.querySelectorAll('.contenido-item');

        draggables.forEach(draggable => {
            const postId = draggable.getAttribute('data-id');
            const estadoOriginalPost = estadoOriginal[postId];
            const columnaOriginal = document.querySelector(`.kanban-column[data-status="${estadoOriginalPost}"] .kanban-items`);

            // Mover el contenido visualmente a su columna original
            columnaOriginal.appendChild(draggable);

            // Eliminar cualquier cambio pendiente relacionado con esta publicación
            cambiosPendientes = cambiosPendientes.filter(cambio => cambio.id !== postId);
            rechazosPendientes = rechazosPendientes.filter(cambio => cambio.id !== postId);
        });
    });
    
    setupDraggables();
    guardarEstadoInicial();
});
