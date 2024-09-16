
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView,DetailView
from categories.models import Categorias
from content.models import Contenido
from content.views import replace_pdf_image_with_link
from django.db.models import Q, Count
from django.contrib.auth.models import User 
from django.core.paginator import Paginator

def home(request):
    """
    Vista para la página de inicio.

    Esta vista renderiza la página de inicio del sitio web, mostrando el contenido 
    filtrado por el estado "Publicado" y ordenado por la fecha de publicación. También
    reemplaza imágenes en archivos PDF con enlaces en el cuerpo del contenido.

    :param request: HttpRequest - La solicitud HTTP que se recibe.

    :return: HttpResponse - La respuesta HTTP que contiene la página de inicio renderizada.
    """
    categorias_restringidas = ['GR', 'PA']
    
    contenido = Contenido.objects.filter(estado="Publicado").order_by("fecha_publicacion")
    
    


    for c in contenido:
        c.cuerpo = replace_pdf_image_with_link(c.cuerpo)

    return render(request, 'home/contenido_home.html',{"contenidos":contenido,"categorias_restringidas":categorias_restringidas})

def buscar_contenido(request):
    query = request.GET.get('q', '')
    categorias = request.GET.getlist('categorias')
    autores = request.GET.getlist('autores')
    
    resultados = Contenido.objects.filter(estado='Publicado')

    if query:
        resultados = resultados.filter(
            Q(titulo__icontains=query) |
            Q(autor__username__icontains=query) |
            Q(categoria__nombre_categoria__icontains=query)
        )

    if categorias:
        resultados = resultados.filter(categoria__id__in=categorias)

    if autores:
        resultados = resultados.filter(autor__username__in=autores)

    sugerencias = []
    if not resultados.exists():
        sugerencias = Contenido.objects.filter(estado='Publicado')[:5]
    context = {
        'resultados': resultados,
        'sugerencias': sugerencias,
        'query': query,
        'categorias': Categorias.objects.all(),
        'autores': User.objects.filter(contenido__isnull=False).distinct(),
    }

    return render(request, 'buscar_resultados.html', context)