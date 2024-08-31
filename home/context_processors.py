from categories.models import Categorias 

def categorias_context(request):
    """
    Un context processor es una función que recibe un objeto request y devuelve un diccionario con los datos que se quieren añadir al contexto de la plantilla.
    """
    categorias = Categorias.objects.all()
    categorias_list = list(categorias.values('nombre_categoria'))
    return {
        'categorias': categorias_list
    }