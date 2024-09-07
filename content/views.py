from distutils.version import Version
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from content.models import Contenido
from .forms import ContenidoForm, EditarContenidoForm

from django.views.generic import FormView
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
        contenido_id = self.kwargs.get('contenido_id')
        if contenido_id:
            contenido = Contenido.objects.get(id=contenido_id)
            context['versiones'] = contenido.versiones.all()
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
        elif contenido.estado == 'Edicion':
            contenido.estado = 'Publicar'
            contenido.save()
            messages.success(self.request, "El contenido ha sido enviado a publicacion")
        elif contenido.estado == 'Publicar':
            contenido.estado = 'Publicado'
            """ chequear la fecha de publicacion del contenido """
            contenido.activo=True
            contenido.save()
            messages.success(self.request, "El contenido ha sido publicado.")
        else:
            messages.error(self.request, "Se produjo un error.")

        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('/')



@login_required
@permission_required('permissions.editar_contenido', raise_exception=True)
def editar_contenido(request, id):
    """
    Vista que permite a un editor, editar un contenido en particular
    :param request: Objeto de solicitud HTTP
    :id: id del contenido a editar
    
    return: Respuesta HTTP que confirma la edicion del contenido
    """
    contenido = get_object_or_404(Contenido, id=id)
    
    if request.method == 'POST':
        form = EditarContenidoForm(request.POST, instance=contenido)
        
        if form.is_valid():
            form.save()
            return redirect('content:vista_editor')  
    else:
        form = EditarContenidoForm(instance=contenido)  
    
    return render(request, 'content/editar_contenido.html', {'form': form})
    
    
@permission_required('permissions.editar_contenido',raise_exception=True)
def vista_Editor(request):
    """
    Vista que lista los contenidos de un editor
    :param request: Objeto de solicitud HTTP
    
    returns: Respuesta HTTP que muestra la lista de contenidos
    """
    
    contenidos=Contenido.objects.filter(estado='Edicion')
    
    return render(request,'content/vista_editor.html',{'contenidos':contenidos})



@login_required
@permission_required('permissions.publicar_contenido', raise_exception=True)
def vista_Publicador(request):
    """
    Vista que lista los contenidos disponibles para un publicador
    :param request: Objeto de solicitud HTTP
    
    return: Respuesta HTTP que muestra la lista de contenidos
    """
    
    contenidos=Contenido.objects.filter(estado='A Publicar')
    
    return render(request,'content/vista_publicador.html',{'contenidos':contenidos})



def a_Publicar(request,id):
    """
    Funcion que permite cambiar el estado de un contenido a "a Publicar"
    paraam request: objeto http de solicitud
    :id: id del contenido a cambiar de estado
    """
    
    contenido=Contenido.objects.get(id=id)
    contenido.estado="A Publicar"
    contenido.save()
    
    return render(request, 'content/vista_publicador.html', {'contenidos': contenido})


def inactivar_contenido(request, id):
    
    """
    Vista que permite a un publicaor, inactivar un contenido
    :param request: Objeto de solicitud HTTP
    :id: id del contenido a inactivar
    
    return: Respuesta HTTP que confirma la publicacion del contenido
    """
    
    contenido = Contenido.objects.get(id=id)
    contenido.estado="Inactivado"
    contenido.save() 