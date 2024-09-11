from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CategoriaForm
from .models import Categorias
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, TemplateView, DetailView
from content.models import Contenido

class CrearCategoriaView(View):
    form_class = CategoriaForm
    template_name = 'categories/new_category.html'

    def get(self, request):
        form = self.form_class()
        categorias = Categorias.objects.all().order_by('-prioridad','pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'create',
            'categorias': categorias
        })

    def post(self, request):
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
    form_class = CategoriaForm
    template_name = 'categories/new_category.html'

    def get(self, request, pk):
        categoria = get_object_or_404(Categorias, pk=pk)
        form = self.form_class(instance=categoria)
        categorias = Categorias.objects.all().order_by('-prioridad','pk')
        return render(request, self.template_name, {
            'form': form,
            'action': 'edit',
            'categorias': categorias
        })

    def post(self, request, pk):
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
        messages.success(request, 'Categoría eliminada con éxito', extra_tags='categoria')
        return redirect('categories:manage')


class ListarCategoriasView(TemplateView):
    """
    Vista para mostrar una lista de categorías y un modal si es necesario.
    """
    template_name = 'categories/listar_categorias.html'

    def get_context_data(self, **kwargs):
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

    Esta vista renderiza una plantilla que muestra los detalles de una categoría
    específica, incluyendo todos los contenidos asociados a ella.
    """
    model = Categorias
    template_name = 'categories/detalle_categoria.html'
    context_object_name = 'categoria'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los contenidos asociados a esta categoría
        contenidos = Contenido.objects.filter(categoria=self.object, estado='Publicado')
        context['contenidos'] = contenidos
        return context
