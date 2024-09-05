from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

from .forms import ContenidoForm

class CrearContenido(LoginRequiredMixin, FormView, PermissionRequiredMixin):
    template_name = "content/crear_contenido.html"
    form_class = ContenidoForm
    permission_required = 'permissions.crear_contenido'

    def get_form_kwargs(self):
        kwargs = super(CrearContenido, self).get_form_kwargs()
        kwargs['autor'] = self.request.user
        return kwargs

    def form_valid(self, form):
        
        form.save()
        messages.success(self.request, "Contenido creado con éxito.")
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Define la URL de redirección después de que el formulario se haya procesado correctamente.

        Returns:
            str: La URL a la que se redirige al usuario.
        """
        return self.request.path
