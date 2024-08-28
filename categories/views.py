from django.views.generic import FormView, ListView
from django.contrib import messages
from .forms import CategoriaForm
from .models import Categorias

class CrearCategoriaView(FormView):
    template_name = "categories/new_category.html"
    form_class = CategoriaForm

    def form_valid(self, form):
        tipo_categoria_cargar = form.cleaned_data['tipo_categoria']
        precio_cargar = 20000 if tipo_categoria_cargar == 'PA' else None

        Categorias.objects.create(
            nombre_categoria=form.cleaned_data['nombre_categoria'],
            descripcion=form.cleaned_data['descripcion'],
            descripcion_corta=form.cleaned_data['descripcion_corta'],
            moderada=form.cleaned_data['moderada'],
            tipo_categoria=tipo_categoria_cargar,
            precio=precio_cargar
        )
        messages.success(self.request, 'Categoría creada con éxito.', extra_tags='categoria')

        # Redirige a la misma vista para mostrar el mensaje y limpiar el formulario
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path  # Redirige a la misma página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categorias.objects.all()
        return context

class CategoriaListView(ListView):
    model = Categorias
    template_name = "categories/new_category.html"
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoriaForm()  # Incluir el formulario de creación
        return context
