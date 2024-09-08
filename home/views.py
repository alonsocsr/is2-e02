
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView,DetailView
from categories.models import Categorias
from content.models import Contenido

def home_users(request):
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
    
    contenido = Contenido.objects.filter(estado="Publicado")
 
        

    return render(request, 'home/contenido_home.html',{"contenidos":contenido})
def landing(request):
    """
      Vista para la página de landing del sito web.

      Esta vista renderiza la página de inicio del sitio web para usuarios no registrados.

      Params:
      -----------
      request : HttpRequest
          La solicitud HTTP que se recibe.

      Returns:
      --------
      HttpResponse
          La respuesta HTTP que contiene la página landing del sitio.
    """
    
    
    categorias_publicas = Categorias.objects.filter(tipo_categoria='PU')

    contenido = Contenido.objects.filter(estado="Publicado", categoria__in=categorias_publicas)
   

    return render(request, 'home/contenido_visitantes.html',{"contenidos":contenido})

""" def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('landing') """