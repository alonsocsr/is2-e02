from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CategoriaForm
from .models import Categorias
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, TemplateView, DetailView
from content.models import Contenido

class CrearCategoriaView(View):
    """
    Vista para crear una nueva categoría.

    Esta vista maneja la creación de una nueva categoría. En el método `GET`, muestra un formulario vacío para la creación de una nueva categoría. En el método `POST`, procesa la creación de la categoría y valida si se excede el límite de categorías con prioridad.

    :cvar form_class: CategoriaForm - El formulario usado para crear una categoría.
    :cvar template_name: str - Nombre de la plantilla utilizada para el formulario de creación.
    """
    form_class = CategoriaForm
    template_name = 'categories/new_category.html'

    def get(self, request):
        """
        Muestra el formulario para la creación de una nueva categoría.

        :param request: HttpRequest - La solicitud HTTP GET.
        :return: HttpResponse - Respuesta renderizada con el formulario de creación y la lista de categorías.
        """
        form = self.form_class()
        categorias = Categorias.objects.all().order_by('-prioridad','pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'create',
            'categorias': categorias
        })

    def post(self, request):
        """
        Procesa el formulario para crear una nueva categoría.

        Valida el formulario y crea la categoría si los datos son válidos. También valida si se ha alcanzado el límite de categorías con prioridad.

        :param request: HttpRequest - La solicitud HTTP POST con los datos del formulario.
        :return: HttpResponse - Redirección a la vista de gestión de categorías con un mensaje de éxito o error.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            # Validar límite de categorías con prioridad
            if form.cleaned_data['prioridad']:
                if Categorias.objects.filter(prioridad=True).count() >= 5:
                    messages.error(request, 'No se pueden crear más de 5 categorías con prioridad.', extra_tags='categoria')
                else:
                    form.save()
                    messages.success(request, 'Categoría creada con éxito.', extra_tags='categoria')
                    return redirect('categories:manage')
            else:
                form.save()
                messages.success(request, 'Categoría creada con éxito.', extra_tags='categoria')
                return redirect('categories:manage')

        categorias = Categorias.objects.all().order_by('-prioridad','pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'create',
            'categorias': categorias
        })


class ModificarCategoriaView(View):
    """
    Vista para modificar una categoría existente.

    Esta vista maneja la modificación de una categoría existente. En el método `GET`, muestra un formulario con los datos de la categoría a modificar. En el método `POST`, procesa la modificación de la categoría y valida si se excede el límite de categorías con prioridad.

    :cvar form_class: CategoriaForm - El formulario usado para modificar una categoría.
    :cvar template_name: str - Nombre de la plantilla utilizada para el formulario de modificación.
    """
    form_class = CategoriaForm
    template_name = 'categories/new_category.html'

    def get(self, request, pk):
        """
        Muestra el formulario para la modificación de una categoría existente.

        :param request: HttpRequest - La solicitud HTTP GET.
        :param pk: int - El identificador primario de la categoría a modificar.
        :return: HttpResponse - Respuesta renderizada con el formulario de modificación y la lista de categorías.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        form = self.form_class(instance=categoria)
        categorias = Categorias.objects.all().order_by('-prioridad','pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'edit',
            'categorias': categorias
        })

    def post(self, request, pk):
        """
        Procesa el formulario para modificar una categoría existente.

        Valida el formulario y modifica la categoría si los datos son válidos. También valida si se ha alcanzado el límite de categorías con prioridad.

        :param request: HttpRequest - La solicitud HTTP POST con los datos del formulario.
        :param pk: int - El identificador primario de la categoría a modificar.
        :return: HttpResponse - Redirección a la vista de gestión de categorías con un mensaje de éxito o error.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        form = self.form_class(request.POST, instance=categoria)
        if form.is_valid():
            # Validar límite de categorías con prioridad
            if form.cleaned_data['prioridad']:
                if Categorias.objects.filter(prioridad=True).exclude(pk=categoria.pk).count() >= 5:
                    messages.error(request, 'No se pueden tener más de 5 categorías con prioridad.', extra_tags='categoria')
                else:
                    form.save()
                    messages.success(request, 'Categoría modificada con éxito.', extra_tags='categoria')
                    return redirect('categories:manage')
            else:
                form.save()
                messages.success(request, 'Categoría modificada con éxito.', extra_tags='categoria')
                return redirect('categories:manage')

        categorias = Categorias.objects.all().order_by('-prioridad','pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'edit',
            'categorias': categorias
        })

class EliminarCategoriaView(View):
    """
    Vista para eliminar una categoría existente.

    Esta vista maneja la eliminación de una categoría. Muestra una confirmación en el método `GET` y procesa la eliminación en el método `POST`.

    :cvar template_name: str - Nombre de la plantilla utilizada para confirmar la eliminación.
    """
    template_name = 'categories/delete_category.html'

    def get(self, request, pk):
        """
        Muestra la confirmación para eliminar una categoría.

        Obtiene la categoría especificada por `pk` y muestra una plantilla de confirmación de eliminación.

        :param request: HttpRequest - La solicitud HTTP GET.
        :param pk: int - El identificador primario de la categoría a eliminar.
        :return: HttpResponse - Respuesta renderizada con la plantilla de confirmación de eliminación.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        return render(request, self.template_name, {'categoria': categoria})

    def post(self, request, pk):
        """
        Procesa la eliminación de una categoría existente.

        Elimina la categoría especificada por `pk` y muestra un mensaje de éxito. Redirige al usuario a la vista de gestión de categorías.

        :param request: HttpRequest - La solicitud HTTP POST para confirmar la eliminación.
        :param pk: int - El identificador primario de la categoría a eliminar.
        :return: HttpResponse - Redirección a la vista de gestión de categorías con un mensaje de éxito.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        nombre_categoria = categoria.nombre_categoria
        categoria.delete()
        messages.success(request, 'Categoría eliminada con éxito', extra_tags='categoria')
        return redirect('categories:manage')


class ListarCategoriasView(TemplateView):
    """
    Vista para mostrar una lista de categorías y un modal si es necesario.

    Esta vista renderiza una plantilla con una lista de todas las categorías y, opcionalmente, muestra un modal si se solicita mediante parámetros en la solicitud.

    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la lista de categorías.
    """
    template_name = 'categories/listar_categorias.html'

    def get_context_data(self, **kwargs):
        """
        Proporciona el contexto para la plantilla de lista de categorías.

        Incluye una lista de categorías y verifica si se debe mostrar un modal.

        :param \**kwargs: Parámetros adicionales que se pasan al método.
        :return: dict - Contexto para la plantilla, incluyendo la lista de categorías, el estado del modal y la categoría específica si se solicita.
        """
        context = super().get_context_data(**kwargs)
        categorias = Categorias.objects.all().order_by('id')
        categorias_list = list(categorias.values('id', 'descripcion', 'nombre_categoria', 'tipo_categoria', 'precio'))

        # Verificar si se debe mostrar el modal
        mostrar_modal = self.request.GET.get('modal') == 'true'
        categoria_id = self.request.GET.get('categoria_id')
        categoria = None
        if categoria_id:
            try:
                categoria = Categorias.objects.get(id=categoria_id)
            except Categorias.DoesNotExist:
                categoria = None

        context.update({
            'categorias': categorias_list,
            'mostrar_modal': mostrar_modal,
            'categoria': categoria
        })
        return context

class DetalleCategoriaView(DetailView):
    """
    Vista para mostrar los detalles de una categoría.

    Esta vista renderiza una plantilla que muestra los detalles de una categoría específica, incluyendo todos los contenidos asociados a ella.

    :cvar model: Categorias - El modelo de la categoría que se muestra.
    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar los detalles de la categoría.
    :cvar context_object_name: str - Nombre del contexto que contiene la categoría.
    """
    model = Categorias
    template_name = 'categories/detalle_categoria.html'
    context_object_name = 'categoria'

    def get_context_data(self, **kwargs):
        """
        Proporciona el contexto para la plantilla de detalles de una categoría.

        Incluye todos los contenidos asociados a la categoría específica.

        :param \**kwargs: Parámetros adicionales que se pasan al método.
        :return: dict - Contexto para la plantilla, incluyendo los detalles de la categoría y los contenidos asociados.
        """
        context = super().get_context_data(**kwargs)
        # Obtener todos los contenidos asociados a esta categoría
        contenidos = Contenido.objects.filter(categoria=self.object, estado='Publicado')
        context['contenidos'] = contenidos
        return context
