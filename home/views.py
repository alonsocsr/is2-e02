from django.shortcuts import render

def home(request):
  """
    Vista para la página de inicio.

    Esta vista renderiza la página de inicio del sitio web.

    Parámetros:
    -----------
    request : HttpRequest
        La solicitud HTTP que se recibe.

    Returns:
    --------
    HttpResponse
        La respuesta HTTP que contiene la página de inicio.
    """
  return render(request, 'home/home.html')