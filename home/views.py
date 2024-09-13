
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView,DetailView
from categories.models import Categorias
from content.models import Contenido
from content.views import replace_pdf_image_with_link

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