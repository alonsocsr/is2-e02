from categories.models import Categorias 

def categorias_context(request):
    """
    Un context processor es una función que recibe un objeto request y devuelve un diccionario con los datos que se quieren añadir al contexto de la plantilla.
    """
    categorias_interes_ids = []
    categorias_suscritas_ids = []
    categorias = Categorias.objects.all().order_by('id')
    categorias_list = list(categorias.values('id','descripcion','nombre_categoria', 'tipo_categoria', 'precio'))
    if request.user.is_authenticated:
        categorias_interes_ids = request.user.profile.categorias_interes.values_list('id', flat=True)
        categorias_suscritas_ids = request.user.profile.suscripciones.values_list('id', flat=True)


    return {
        'categorias': categorias_list,
        'categorias_interes_ids': categorias_interes_ids,
        'categorias_suscritas_ids': categorias_suscritas_ids
    }

def is_only_suscriptor(request):
    """
    Recibe un objeto request y devuelve si el usuario es solamente un suscriptor o no
    """
    if request.user.is_authenticated:
        is_suscriptor = request.user.groups.filter(name='Suscriptor').exists() and request.user.groups.count() == 1
        return {'is_only_suscriptor': is_suscriptor}
    
    return {'is_only_suscriptor': False}
