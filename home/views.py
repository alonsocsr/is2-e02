
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView,DetailView
from categories.models import Categorias
from content.models import Contenido
from content.views import replace_pdf_image_with_link

def home(request):
    """
      Vista para la página de inicio.

      Esta vista renderiza la página de inicio del sitio web.

      Params:
      -----------
      request : HttpRequest
          La solicitud HTTP que se recibe.

      Returns:
      --------
      HttpResponse
          La respuesta HTTP que contiene la página de inicio.
    """
    categorias_restringidas = ['GR', 'PA']
    
    contenido = Contenido.objects.filter(estado="Publicado")
    
    


    for c in contenido:
        c.cuerpo = replace_pdf_image_with_link(c.cuerpo)

    return render(request, 'home/contenido_home.html',{"contenidos":contenido,"categorias_restringidas":categorias_restringidas})