from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib import messages
from .forms import CategoriaForm
from .models import Categorias
from django.shortcuts import get_object_or_404, redirect

class CrearCategoriaView(View):
    """
    Vista para crear una nueva categoría.

    Esta `View` maneja la creación de una nueva categoría. Se encarga de mostrar un formulario
    vacío en el método `GET` y de procesar el formulario en el método `POST`.

    Atributos:
        form_class (forms.ModelForm): Clase del formulario utilizada para la creación.
        template_name (str): Nombre de la plantilla utilizada para renderizar el formulario.
    """
    form_class = CategoriaForm
    template_name = 'categories/new_category.html'

    def get(self, request):
        """
        Muestra el formulario para crear una nueva categoría.

        Obtiene y renderiza un formulario vacío para crear una nueva categoría, junto con la lista
        de todas las categorías existentes.

        Args:
            request (HttpRequest): La solicitud HTTP GET.

        Returns:
            HttpResponse: Respuesta renderizada con el formulario de creación.
        """
        form = self.form_class()
        categorias = Categorias.objects.all().order_by('pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'create',
            'categorias': categorias
        })

    def post(self, request):
        """
        Procesa el formulario de creación de una nueva categoría.

        Valida y guarda el formulario enviado. En caso de éxito, muestra un mensaje de éxito y
        redirige al usuario a la vista de gestión de categorías. Si el formulario no es válido,
        vuelve a mostrar el formulario con los errores.

        Args:
            request (HttpRequest): La solicitud HTTP POST con datos del formulario.

        Returns:
            HttpResponse: Respuesta renderizada con el formulario, si hay errores, o redirección
            en caso de éxito.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.', extra_tags='categoria')
            return redirect('categories:manage')

        categorias = Categorias.objects.all().order_by('pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'create',
            'categorias': categorias
        })


class ModificarCategoriaView(View):
    """
    Vista para actualizar una categoría existente.

    Este `View` maneja la actualización de una categoría existente. Se encarga de mostrar el
    formulario con los datos actuales en el método `GET` y de procesar el formulario en el método `POST`.

    Atributos:
        form_class (forms.ModelForm): Clase del formulario utilizada para la actualización.
        template_name (str): Nombre de la plantilla utilizada para renderizar el formulario.
    """
    form_class = CategoriaForm
    template_name = 'categories/new_category.html'

    def get(self, request, pk):
        """
        Muestra el formulario para actualizar una categoría existente.

        Obtiene la categoría especificada por `pk` y renderiza el formulario con los datos actuales
        de la categoría. También se incluye la lista de todas las categorías existentes.

        Args:
            request (HttpRequest): La solicitud HTTP GET.
            pk (int): El id de la categoría a actualizar.

        Returns:
            HttpResponse: Respuesta renderizada con el formulario de actualización.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        form = self.form_class(instance=categoria)
        categorias = Categorias.objects.all().order_by('pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'edit',
            'categorias': categorias
        })

    def post(self, request, pk):
        """
        Procesa el formulario para actualizar una categoría existente.

        Valida y guarda el formulario enviado con los datos de la categoría existente. En caso de
        éxito, muestra un mensaje de éxito y redirige al usuario a la vista de gestión de categorías.
        Si el formulario no es válido, vuelve a mostrar el formulario con los errores.

        Args:
            request (HttpRequest): La solicitud HTTP POST con datos del formulario.
            pk (int): El identificador primario de la categoría a actualizar.

        Returns:
            HttpResponse: Respuesta renderizada con el formulario, si hay errores, o redirección
            en caso de éxito.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        form = self.form_class(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría modificada con éxito.', extra_tags='categoria')
            return redirect('categories:manage')

        categorias = Categorias.objects.all().order_by('pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'edit',
            'categorias': categorias
        })

class EliminarCategoriaView(View):
    """
    Vista para eliminar una categoría existente.

    Este `View` maneja la eliminación de una categoría. Muestra una confirmación en el método `GET`
    y procesa la eliminación en el método `POST`.

    Atributos:
        template_name (str): Nombre de la plantilla utilizada para confirmar la eliminación.
    """
    template_name = 'categories/delete_category.html'

    def get(self, request, pk):
        """
        Muestra la confirmación para eliminar una categoría.

        Obtiene la categoría especificada por `pk` y muestra una plantilla de confirmación de eliminación.

        Args:
            request (HttpRequest): La solicitud HTTP GET.
            pk (int): El identificador primario de la categoría a eliminar.

        Returns:
            HttpResponse: Respuesta renderizada con la plantilla de confirmación de eliminación.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        return render(request, self.template_name, {'categoria': categoria})

    def post(self, request, pk):
        """
        Procesa la eliminación de una categoría existente.

        Elimina la categoría especificada por `pk` y muestra un mensaje de éxito. Redirige al
        usuario a la vista de gestión de categorías.

        Args:
            request (HttpRequest): La solicitud HTTP POST para confirmar la eliminación.
            pk (int): El identificador primario de la categoría a eliminar.

        Returns:
            HttpResponse: Redirección a la vista de gestión de categorías con un mensaje de éxito.
        """
        categoria = get_object_or_404(Categorias, pk=pk)
        nombre_categoria = categoria.nombre_categoria
        categoria.delete()
        messages.success(request, 'Categoría eliminada con éxito')
        return redirect('categories:manage')

from django.views.generic import TemplateView

class ListarCategoriasView(TemplateView):
    """
    Vista para mostrar una lista de categorías.

    Esta vista renderiza una plantilla que muestra todas las categorías disponibles
    en la base de datos.
    """
    template_name = 'categories/listar_categorias.html'
