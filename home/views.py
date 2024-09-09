
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView,DetailView
from categories.models import Categorias
from content.models import Contenido

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
    if request.user.is_authenticated:
        contenido = Contenido.objects.filter(estado="Publicado")
    else:
        categorias_publicas = Categorias.objects.filter(tipo_categoria='PU')
        contenido = Contenido.objects.filter(estado="Publicado", categoria__in=categorias_publicas)

    return render(request, 'home/contenido_home.html',{"contenidos":contenido})