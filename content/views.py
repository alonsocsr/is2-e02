from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import redirect

from .forms import ContenidoForm
from .models import Version
from .models import Contenido

class ContenidoBorradorList(LoginRequiredMixin, ListView):
    model = Contenido
    template_name = 'content/list_borrador.html'
    context_object_name = 'borradores'
    
    def get_queryset(self):
        return Contenido.objects.filter(autor=self.request.user, estado='Borrador')
    

class CrearContenido(LoginRequiredMixin, FormView, PermissionRequiredMixin):
    template_name = "content/crear_contenido.html"
    form_class = ContenidoForm
    permission_required = 'permissions.crear_contenido'

    def get_form_kwargs(self):
        kwargs = super(CrearContenido, self).get_form_kwargs()
        kwargs['autor'] = self.request.user
        
        #si estamos editando un contenido existente
        contenido_id = self.kwargs.get('contenido_id', None)
        if contenido_id:
            contenido = Contenido.objects.get(id=contenido_id, autor=self.request.user)
            kwargs['instance'] = contenido
            kwargs['initial'] = {
                'titulo': contenido.titulo,
                'resumen': contenido.resumen,
                'cuerpo': contenido.cuerpo,
                'categoria': contenido.categoria,
                'fecha_publicacion': contenido.fecha_publicacion.isoformat(),
                'vigencia': contenido.vigencia.isoformat()
            }

        #si estamos editando una version
        version_id = self.request.GET.get('version_id')
        if version_id:
            try:
                version = Version.objects.get(id=version_id)
                kwargs['initial'] = {
                    'titulo': version.titulo,
                    'resumen': version.resumen,
                    'cuerpo': version.cuerpo,
                    'categoria': version.contenido.categoria,
                    'fecha_publicacion': version.fecha_publicacion.isoformat(),
                    'vigencia': version.vigencia.isoformat()
                }
                messages.success(self.request, "Se ha seleccionado la version")
            except Version.DoesNotExist:
                pass
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(CrearContenido, self).get_context_data(**kwargs)
        contenido_id = self.kwargs.get('contenido_id')  # Assuming content ID is passed as a URL parameter
        if contenido_id:
            contenido = Contenido.objects.get(id=contenido_id)
            context['versiones'] = contenido.versiones.all()  # Pass the versions to the template
        return context

    def form_valid(self, form):
        contenido = form.save(commit=False)
        try:
            contenido.save()
            contenido.save_version()
            messages.success(self.request, "Contenido guardado y versión creada con éxito.")
        except ValueError:
            messages.error('El título ya existe')    
        

        self.object = contenido
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Define la URL de redirección después de que el formulario se haya procesado correctamente.

        Returns:
            str: La URL a la que se redirige al usuario.
        """
        return reverse('crear_contenido', kwargs={'contenido_id': self.object.id})

class CambiarEstadoView(UpdateView):
    model = Contenido
    fields = []
    template_name = "content/cambiar_estado.html"

    def form_valid(self, form):
        contenido = form.instance
        if contenido.estado == 'Borrador':
            contenido.estado = 'Edicion'
            contenido.save()
            messages.success(self.request, "El contenido ha sido enviado a Edición.")
        else:
            messages.error(self.request, "El contenido no está en Borrador.")
        
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('/')