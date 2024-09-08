from categories.models import Categorias 

def categorias_context(request):
    """
    Un context processor es una función que recibe un objeto request y devuelve un diccionario con los datos que se quieren añadir al contexto de la plantilla.
    """
    categorias_interes_ids = []
    categorias = Categorias.objects.all().order_by('id')
    categorias_list = list(categorias.values('id','descripcion','nombre_categoria', 'tipo_categoria'))
    if request.user.is_authenticated:
        categorias_interes_ids = request.user.profile.categorias_interes.values_list('id', flat=True)

    return {
        'categorias': categorias_list,
        'categorias_interes_ids': categorias_interes_ids
    }