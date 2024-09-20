
from django.views.generic import ListView
from categories.models import Categorias
from content.models import Contenido
from content.views import replace_pdf_image_with_link
from django.db.models import Q
from django.contrib.auth.models import User
from decouple import config
from django.utils import timezone

class HomeView(ListView):
    """
    Vista para la página de inicio.

    Esta vista renderiza la página de inicio del sitio web, mostrando el contenido 
    filtrado por el estado "Publicado" y ordenado por la fecha de publicación. También
    reemplaza imágenes en archivos PDF con enlaces en el cuerpo del contenido.

    :param request: HttpRequest - La solicitud HTTP que se recibe.

    :return: HttpResponse - La respuesta HTTP que contiene la página de inicio renderizada.
    """
    model = Contenido
    template_name = 'home/contenido_home.html'
    context_object_name = 'contenidos'

    def verificar_estados_contenidos(self):
        """
        Verifica y actualiza los estados de los contenidos basados en la fecha de publicación y vigencia.
        """
        fecha_actual = timezone.now().date()
        
        # Publicar contenidos cuya fecha de publicación haya llegado y aún no estén activos
        contenidos_a_publicar = Contenido.objects.filter(
            estado='Publicado',
            activo=False,
            fecha_publicacion__lte=fecha_actual
        )
        for contenido in contenidos_a_publicar:
            contenido.activo = True
            contenido.save()

        # Inactivar contenidos cuya fecha de vigencia haya pasado
        contenidos_a_inactivar = Contenido.objects.filter(
            estado='Publicado',
            activo=True,
            vigencia__lte=fecha_actual
        )
        for contenido in contenidos_a_inactivar:
            contenido.estado = 'Inactivo'
            contenido.activo = False
            contenido.save()


    def get_queryset(self):
        """
        Filtra los contenidos por estado 'Publicado' y los ordena por la fecha de publicación.
        También reemplaza imágenes en archivos PDF con enlaces en el cuerpo del contenido.
        """

        # Verificar y actualizar los estados de los contenidos
        self.verificar_estados_contenidos()

        queryset = Contenido.objects.filter(estado="Publicado", activo=True).order_by("fecha_publicacion")
        # Reemplazar imágenes en archivos PDF con enlaces
        for c in queryset:
            c.cuerpo = replace_pdf_image_with_link(c.cuerpo)
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Agrega 'categorias_restringidas', 'mostrar_modal' y otras variables al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)

        # Añadir categorías restringidas
        context['categorias_restringidas'] = ['GR', 'PA']

        # Verificar si el modal debe mostrarse
        mostrar_modal = self.request.GET.get('modal') == 'true'
        context['mostrar_modal'] = mostrar_modal
            
        if mostrar_modal:
            categoria_id = self.request.GET.get('categoria_id')
            if categoria_id:
                categoria = Categorias.objects.filter(id=categoria_id).first()
                if categoria:
                    context['categoria'] = categoria
                    context['contenidos'] = Contenido.objects.filter(categoria=categoria, estado='Publicado', activo=True)
            context['categoria_id'] = categoria_id
        else:
            context['mostrar_modal'] = False

        # Agregar la clave pública de Stripe al contexto
        context['STRIPE_PUBLIC_KEY'] = config('STRIPE_PUBLIC_KEY')
        
        return context



class BuscarContenidoView(ListView):
    """
    Vista para buscar contenido publicado en base a una query, categorías y autores.

    Esta vista permite realizar una búsqueda sobre los contenidos filtrados por 
    estado 'Publicado', permitiendo además filtrar por categorías y autores. Si no 
    se encuentran resultados, se sugiere contenido relacionado.

    :param query: str - La consulta de búsqueda introducida por el usuario.
    :param categorias: list - Lista de categorías seleccionadas para el filtro.
    :param autores: list - Lista de autores seleccionados para el filtro.

    :return: HttpResponse - Respuesta con los resultados de la búsqueda y sugerencias si no hay resultados.
    """
    model = Contenido
    template_name = 'buscar_resultados.html'
    context_object_name = 'resultados'

    def get_queryset(self):
        """
        Sobrescribe el método `get_queryset` para filtrar los contenidos según la búsqueda,
        categorías y autores seleccionados.

        :return: QuerySet - Un queryset de contenido filtrado por los parámetros de búsqueda.
        """
        query = self.request.GET.get('q', '')
        categorias = self.request.GET.getlist('categorias')
        autores = self.request.GET.getlist('autores')

        # Filtrar por estado 'Publicado'
        resultados = Contenido.objects.filter(estado='Publicado', activo=True)

        # Filtrar por la query
        if query:
            resultados = resultados.filter(
                Q(titulo__icontains=query) |
                Q(autor__username__icontains=query) |
                Q(categoria__nombre_categoria__icontains=query)
            )

        # Filtrar por categorías
        if categorias:
            resultados = resultados.filter(categoria__id__in=categorias)

        # Filtrar por autores
        if autores:
            resultados = resultados.filter(autor__username__in=autores)

        return resultados

    def get_context_data(self, **kwargs):
        """
        Añade sugerencias y otros datos al contexto de la plantilla. Si no se encuentran 
        resultados, se muestran sugerencias de contenido publicado.

        :param \**kwargs: Parámetros adicionales pasados al método.
        :return: dict - El contexto para renderizar la plantilla con resultados, sugerencias, categorías y autores.
        """
        context = super().get_context_data(**kwargs)

        # Si no hay resultados, agregar sugerencias
        if not context['resultados'].exists():
            context['sugerencias'] = Contenido.objects.filter(estado='Publicado', activo=True)[:5]
        else:
            context['sugerencias'] = []

        # Pasar el resto del contexto adicional
        context['query'] = self.request.GET.get('q', '')
        context['categorias'] = Categorias.objects.all()
        context['autores'] = User.objects.filter(contenido__isnull=False).distinct()

        return context
