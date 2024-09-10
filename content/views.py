from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, FormMixin, UpdateView
from .forms import ContenidoForm, EditarContenidoForm, RechazarContenidoForm, ContenidoReportadoForm
from .models import Version, Contenido, ContenidoReportado   


class VistaAllContenidos(ListView):
    template_name="content/ver_contenidos.html"
    model=Contenido
    ordering=["-fecha_publicacion"]
    context_object_name="all_contenidos"
    
    def get_queryset(self):
        return Contenido.objects.filter(estado="Publicado").order_by("-fecha_publicacion")
    
class VistaContenido(FormMixin, DetailView):
    template_name="content/detalle_contenido.html"
    model=Contenido
    slug_field = 'slug'  
    slug_url_kwarg = 'slug' 

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Contenido, slug=slug)
    
    form_class = ContenidoReportadoForm
    context_object_name="contenido"

    # def get_success_url(self):
    #     return reverse_lazy('detalle_contenido', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.method == 'POST':
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.usuario = self.request.user
        form.instance.contenido = self.get_object()
        messages.success(self.request, "Se reportado el contenido con éxito")
        form.save()
        return super().form_valid(form)
    

     
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
        contenido_id = self.kwargs.get('contenido_id')
        if contenido_id:
            contenido = Contenido.objects.get(id=contenido_id)
            context['versiones'] = contenido.versiones.all()
            context['modo'] = 'editar' 
        else:
            context['modo'] = 'crear'
        return context

    def form_valid(self, form):
        contenido = form.save(commit=False)
        try:
            contenido.save()
            contenido.save_version(None)
            messages.success(self.request, "Contenido guardado y versión creada con éxito.")
        except ValueError:
            messages.error('El título ya existe')    

        self.object = contenido
        return super().form_valid(form)
    
    def get_success_url(self):
        """
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
            contenido.mensaje_rechazo = ''
            messages.success(self.request, "El contenido ha sido enviado a Edición.")
        elif contenido.estado == 'Edicion':
            contenido.estado = 'Publicar'
            contenido.mensaje_rechazo = ''
            messages.success(self.request, "El contenido ha sido enviado a publicacion")
        elif contenido.estado == 'Publicar':
            contenido.estado = 'Publicado'
            contenido.activo=True
            """ chequear la fecha de publicacion del contenido """
            messages.success(self.request, "El contenido ha sido publicado.")

        elif contenido.estado=='Publicado':
            contenido.estado='Inactivo'
            contenido.activo=False
            messages.success(self.request, "El contenido ha sido inactivado")
        else:
            messages.error(self.request, "No se pudo cambiar el estado del contenido")

        contenido.save()
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('/')


class ContenidoEdicionList(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    """
    Vista que lista los contenidos de un editor
    :param request: Objeto de solicitud HTTP
    
    returns: Respuesta HTTP que muestra la lista de contenidos
    """
    model = Contenido
    template_name = 'content/vista_editor.html'
    context_object_name = 'contenidos'
    permission_required = 'permissions.editar_contenido'

    def get_queryset(self):
        return Contenido.objects.filter(
                Q(estado='Edicion') &
                (Q(usuario_editor=self.request.user) | Q(usuario_editor=None))
            )


class EditarContenido(LoginRequiredMixin, FormView, PermissionRequiredMixin):
    template_name = "content/editar_contenido.html"
    form_class = EditarContenidoForm
    permission_required = 'permissions.editar_contenido'

    def get_form_kwargs(self):
        kwargs = super(EditarContenido, self).get_form_kwargs()
        kwargs['usuario_editor'] = self.request.user

        #abre el contenido original
        contenido_id = self.kwargs.get('contenido_id', None)
        if contenido_id:
            contenido = Contenido.objects.get(id=contenido_id)
            kwargs['instance'] = contenido
            kwargs['initial'] = {
                'titulo': contenido.titulo,
                'resumen': contenido.resumen,
                'cuerpo': contenido.cuerpo,
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
                }
                messages.success(self.request, "Se ha seleccionado la version")
            except Version.DoesNotExist:
                pass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EditarContenido, self).get_context_data(**kwargs)
        contenido_id = self.kwargs.get('contenido_id')
        editor = self.request.user
        if contenido_id:
            try:
                contenido = Contenido.objects.get(id=contenido_id, usuario_editor=editor)
                context['versiones'] = contenido.versiones.filter(editor=editor)
            except Contenido.DoesNotExist:
                context['versiones'] = None
        return context

    def form_valid(self, form):
        contenido = form.save(commit=False)
        try:
            contenido.save()
            contenido.save_version(self.request.user)
            messages.success(self.request, "Contenido guardado y versión creada con éxito.")
        except ValueError:
            messages.error('El título ya existe')    

        self.object = contenido
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Returns:
            str: La URL a la que se redirige al usuario.
        """
        return reverse('editar_contenido', kwargs={'contenido_id': self.object.id})


class ContenidoPublicarList(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    """
    Vista que lista los contenidos de un editor
    :param request: Objeto de solicitud HTTP
    
    returns: Respuesta HTTP que muestra la lista de contenidos
    """
    model = Contenido
    template_name = 'content/vista_publicador.html'
    context_object_name = 'contenidos'
    permission_required = 'permissions.publicar_contenido'

    def get_queryset(self):
        return Contenido.objects.filter(estado='Publicar')


class RechazarContenido(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Contenido
    form_class = RechazarContenidoForm
    permission_required = 'permissions.rechazar_contenido'
    
    def form_valid(self, form):
        contenido = form.save(commit=False)
        if contenido.estado == 'Publicar':
            contenido.estado = 'Edicion'
            messages.success(self.request, "El contenido ha sido enviado a Edicion.")
        elif contenido.estado == 'Edicion':
            contenido.estado = 'Borrador'
            messages.success(self.request, "El contenido ha sido enviado a Borrador.")
        else:
            messages.error(self.request, "Se produjo un error")
        
        contenido.save()
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('/')
        
class InactivarContenido(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Contenido
    fields=[]
    permission_required = 'permissions.inactivar_contenido'
    
    def form_valid(self, form):
        contenido = form.save(commit=False)
        contenido.estado = 'Inactivo'
        contenido.activo = False
        messages.success(self.request, "El contenido ha sido enviado a Edicion.")
        contenido.save()

        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('/')
