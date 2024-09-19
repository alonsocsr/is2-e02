import json
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import FormView, FormMixin, UpdateView
from .forms import ContenidoForm, EditarContenidoForm, RechazarContenidoForm, ContenidoReportadoForm
from .models import Version, Contenido, ContenidoReportado   
import re, json
from django.utils.safestring import mark_safe
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class VistaAllContenidos(ListView):
    """
    Vista para listar todos los contenidos publicados.

    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la lista de contenidos.
    :cvar model: Contenido - El modelo de datos utilizado para mostrar los contenidos.
    :cvar ordering: list - Lista de campos por los cuales se ordenan los contenidos.
    :cvar context_object_name: str - Nombre del contexto para los contenidos en la plantilla.
    """
    template_name="content/ver_contenidos.html"
    model=Contenido
    ordering=["fecha_publicacion"]
    context_object_name="all_contenidos"
    
    def get_queryset(self):
        return Contenido.objects.filter(estado="Publicado").order_by("fecha_publicacion")
    
class VistaContenido(FormMixin, DetailView):
    """
    Vista para mostrar el detalle de un contenido y permitir su reporte.

    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar el detalle del contenido.
    :cvar model: Contenido - El modelo de datos utilizado para mostrar el contenido.
    :cvar slug_field: str - Campo utilizado para buscar el contenido por slug.
    :cvar slug_url_kwarg: str - Nombre del argumento de URL que contiene el slug.
    :cvar form_class: ContenidoReportadoForm - El formulario utilizado para reportar el contenido.
    :cvar context_object_name: str - Nombre del contexto para el contenido en la plantilla.
    """
    template_name="content/detalle_contenido.html"
    model=Contenido
    slug_field = 'slug'  
    slug_url_kwarg = 'slug' 
    form_class = ContenidoReportadoForm
    context_object_name="contenido"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Contenido, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenido'].cuerpo = replace_pdf_image_with_link(context['contenido'].cuerpo)
        
        disqus_shortname = settings.DISQUS_WEBSITE_SHORTNAME
        disqus_identifier = context['contenido'].slug  
        disqus_url = self.request.build_absolute_uri()  

       
        context['disqus_shortname'] = disqus_shortname
        context['disqus_identifier'] = disqus_identifier
        context['disqus_url'] = disqus_url
        return context
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user 
        return kwargs

    def get_success_url(self):
        return reverse('detalle_contenido', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        contenido_reportado = form.save(commit=False)
        contenido_reportado.contenido = self.object
        if self.request.user.is_authenticated:
            contenido_reportado.usuario = self.request.user
            contenido_reportado.email = self.request.user.email
        else:
            email = form.cleaned_data.get('email')
            contenido_reportado.usuario = None 
            contenido_reportado.email=email
            
        contenido_reportado.save()
        messages.success(self.request, "Se ha reportado el contenido con éxito.")
        return redirect(self.get_success_url())
    

     
class ContenidoBorradorList(LoginRequiredMixin, ListView):
    """
    Vista para listar los contenidos en estado de borrador del usuario actual.

    :cvar model: Contenido - El modelo de datos utilizado para mostrar los contenidos.
    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la lista de borradores.
    :cvar context_object_name: str - Nombre del contexto para los borradores en la plantilla.
    """
    model = Contenido
    template_name = 'content/list_borrador.html'
    context_object_name = 'borradores'

    def get_queryset(self):
        return Contenido.objects.filter(autor=self.request.user, estado='Borrador').order_by('fecha_modificacion')
     
class ContenidoInactivadoList(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    """
    Vista para listar los contenidos inactivados, con permisos de acceso requeridos.

    :cvar model: Type[Contenido] - El modelo de datos utilizado para recuperar los contenidos.
    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la lista de contenidos inactivos.
    :cvar context_object_name: str - Nombre del contexto para los contenidos en la plantilla.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    """
    model = Contenido
    template_name = 'content/list_inactivado.html'
    context_object_name = 'contenidos'
    permission_required = 'permissions.inactivar_contenido'

    def get_queryset(self):
        user=self.request.user
        if user.groups.filter(name="Admin").exists():
           return Contenido.objects.filter(estado='Inactivo').order_by('fecha_modificacion')
        elif user.groups.filter(name="Autor").exists():
            return Contenido.objects.filter(autor=self.request.user, estado='Inactivo').order_by('fecha_modificacion')
        else:
            return Contenido.objects.none()

class CrearContenido(LoginRequiredMixin, FormView, PermissionRequiredMixin):
    """
    Vista para crear un nuevo contenido.

    :cvar template_name: str - Nombre de la plantilla utilizada para el formulario de creación de contenido.
    :cvar form_class: ContenidoForm - El formulario utilizado para crear el contenido.
    :cvar permission_required: str - Permiso requerido para crear contenido.
    """
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
                'fecha_publicacion': contenido.fecha_publicacion.isoformat() if contenido.fecha_publicacion is not None else None,
                'vigencia': contenido.vigencia.isoformat() if contenido.vigencia is not None else None
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
                    'fecha_publicacion': version.fecha_publicacion.isoformat() if contenido.fecha_publicacion is not None else None,
                    'vigencia': version.vigencia.isoformat() if contenido.vigencia is not None else None
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
        return reverse('crear_contenido', kwargs={'contenido_id': self.object.id})

class CambiarEstadoView(UpdateView):
    """
    Vista para cambiar el estado de un contenido.

    Esta vista permite cambiar el estado de un contenido basado en su categoría y estado actual.

    :cvar model: Contenido - El modelo del contenido que se está actualizando.
    :cvar fields: list - Lista de campos del modelo a mostrar en el formulario.
    :cvar template_name: str - Nombre de la plantilla utilizada para renderizar el formulario.
    """
    model = Contenido
    fields = []
    template_name = "content/cambiar_estado.html"

    def form_valid(self, form):
        contenido = form.instance
        categoria=contenido.categoria
        if categoria.moderada is False:
            contenido.estado = 'Publicado'
            contenido.activo=True
            contenido.mensaje_rechazo = ''
            """ chequear la fecha de publicacion del contenido """
            messages.success(self.request, "El contenido ha sido publicado.")
        else:
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
    :cvar model: Contenido - El modelo del contenido que se está listando.
    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la lista de contenidos.
    :cvar context_object_name: str - Nombre del contexto que contiene la lista de contenidos.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    
    :returns: Respuesta HTTP que muestra la lista de contenidos
    """
    model = Contenido
    template_name = 'content/vista_editor.html'
    context_object_name = 'contenidos'
    permission_required = 'permissions.editar_contenido'

    def get_queryset(self):
        return Contenido.objects.filter(
                Q(estado='Edicion') &
                (Q(usuario_editor=self.request.user) | Q(usuario_editor=None))
            ).order_by('fecha_modificacion')


class EditarContenido(LoginRequiredMixin, FormView, PermissionRequiredMixin):
    """
    Vista para editar el contenido.

    Esta vista permite al usuario editar un contenido y sus versiones, si es necesario.

    :cvar template_name: str - Nombre de la plantilla utilizada para renderizar el formulario de edición.
    :cvar form_class: type - Clase del formulario utilizado para editar el contenido.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    """
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
    :cvar model: Contenido - El modelo del contenido que se está listando.
    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la lista de contenidos.
    :cvar context_object_name: str - Nombre del contexto que contiene la lista de contenidos.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    
    returns: Respuesta HTTP que muestra la lista de contenidos
    """
    model = Contenido
    template_name = 'content/vista_publicador.html'
    context_object_name = 'contenidos'
    permission_required = 'permissions.publicar_contenido'

    def get_queryset(self):
        return Contenido.objects.filter(estado='Publicar').order_by('fecha_modificacion')


class RechazarContenido(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """
    Vista para rechazar un contenido.

    Esta vista permite cambiar el estado de un contenido a Edición o Borrador, dependiendo de su estado actual.

    :cvar model: Contenido - El modelo del contenido que se está actualizando.
    :cvar form_class: type - Clase del formulario utilizado para rechazar el contenido.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    """
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
    """
    Vista para activar o inactivar un contenido.

    Esta vista permite cambiar el estado de un contenido entre Inactivo y Activo.

    :cvar model: Contenido - El modelo del contenido que se está actualizando.
    :cvar fields: list - Lista de campos del modelo a mostrar en el formulario.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    """
    model = Contenido
    fields=[]
    permission_required = 'permissions.inactivar_contenido'
    
    def form_valid(self, form):
        contenido = form.save(commit=False)
        if contenido.activo:
            contenido.estado = 'Inactivo'
            contenido.activo = False
            messages.success(self.request, "El contenido ha sido Inactivado.")
        else:
            contenido.estado = 'Publicado'
            contenido.activo = True
            messages.success(self.request, "El contenido ha sido Activado.")
        contenido.save()

        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('/')



def replace_pdf_image_with_link(content):
    """
    Reemplaza imágenes en el contenido con enlaces a archivos PDF.

    Esta función busca imágenes que enlazan a archivos PDF y las reemplaza con un enlace al archivo PDF.

    :param content: str - Contenido HTML con imágenes.
    :return: str - Contenido HTML con imágenes reemplazadas por enlaces.
    """
    pattern = r'<img[^>]+src="([^"]+\.pdf)"[^>]*>'
    
    def replace_match(match):
        pdf_url = match.group(1)
        archivo = pdf_url.split('/')[-1]
        return f'<a href="{pdf_url}" target="_blank">{archivo}</a>'
   
    updated_content = re.sub(pattern, replace_match, content)
    
    return updated_content

class VistaContenidosReportados(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    """
    Vista que muestra los contenidos reportados en el sitio web
    cvar model: ContenidoReportado - El modelo de los contenidos reportados.
    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la lista de contenidos reportados.
    :cvar context_object_name: str - Nombre del contexto que contiene la lista de contenidos reportados.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.

    :return: Respuesta HTTP que muestra la lista de contenidos reportados
    """
    model = ContenidoReportado
    template_name = 'content/contenidos_reportados.html'
    context_object_name = 'contenidos'
    permission_required = 'permissions.ver_reportes_contenido'

    def get_queryset(self):
        user=self.request.user
        if user.has_perm('permissions.suspender_cuenta') or user.groups.filter(name="Admin"):
            return ContenidoReportado.objects.all()
        elif user.groups.filter(name="Autor").exists():
            return ContenidoReportado.objects.filter(contenido__autor=user)
        else:
            return ContenidoReportado.objects.none()




@method_decorator(csrf_exempt, name='dispatch')
class TableroKanbanView(LoginRequiredMixin, TemplateView, PermissionRequiredMixin):
    """
    Vista para mostrar el Tablero Kanban.

    Esta vista agrupa el contenido en diferentes columnas según su estado (Borrador, Edición, Publicación, Publicado, Inactivo)
    y permite a los usuarios con los permisos correspondientes mover los contenidos entre estas columnas.

    :cvar template_name: str - Nombre de la plantilla utilizada para renderizar el tablero Kanban.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    
    :return: Respuesta HTTP que muestra el tablero Kanban con los contenidos agrupados por su estado.
    """
    template_name = 'content/tablero_kanban.html'
    permission_required = 'permissions.ver_tablero_kanban'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las publicaciones y agruparlas por estado
        contenido = Contenido.objects.all()
        context['borrador'] = contenido.filter(estado='Borrador')
        context['edicion'] = contenido.filter(estado='Edicion')
        context['publicacion'] = contenido.filter(estado='Publicar')
        context['publicado'] = contenido.filter(estado='Publicado')
        context['inactivo'] = contenido.filter(estado='Inactivo')
        # Obtener los permisos necesarios para mover los contenidos
        context['crear_perm'] = self.request.user.has_perm('permissions.crear_contenido')
        context['editar_perm'] = self.request.user.has_perm('permissions.editar_contenido')
        context['publicar_perm'] = self.request.user.has_perm('permissions.publicar_contenido')
        context['inactivar_perm'] = self.request.user.has_perm('permissions.inactivar_contenido')
        # context['activar_contenido'] = self.request.user.has_perm('permissions.modificar_tablero_kanban')
        return context


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePostStatusView(LoginRequiredMixin, View):
    """
    Vista para actualizar el estado de un contenido en el tablero Kanban.

    Esta vista procesa las solicitudes POST que contienen una lista de cambios en el estado de los contenidos.
    Dependiendo del nuevo estado proporcionado, se actualiza el estado de los contenidos en la base de datos.

    :return: Redirige a la página anterior o al tablero Kanban después de actualizar el estado.
    """
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        cambios = data.get('cambios', [])

        for cambio in cambios:
            post_id = cambio['id']
            new_status = cambio['status']

            # Obtener el contenido y actualizar su estado
            post = Contenido.objects.get(id=post_id)

            if new_status == 'Borrador':
                post.estado = 'Borrador'
            elif new_status == 'Edicion':
                post.estado = 'Edicion'
            elif new_status == 'Publicacion':
                post.estado = 'Publicar'
            elif new_status == 'Publicado':
                post.estado = 'Publicado'
                post.activo = True
                post.mensaje_rechazo = ''
            elif new_status == 'Inactivo':
                post.estado = 'Inactivo'
                post.activo = False

            post.save()

        messages.success(self.request, "Se ha actualizado el tablero kanban con éxito.")




