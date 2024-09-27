from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CategoriaForm
from .models import Categorias
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, TemplateView, DetailView
from content.models import Contenido
from decouple import config
from django.http import JsonResponse
import stripe

stripe.api_key = config('STRIPE_SECRET_KEY')

class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Mixin personalizado para manejar permisos denegados y redirigir al home.
    """
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().handle_no_permission()
    
class CrearCategoriaView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    """
    Vista para crear una nueva categoría.

    Esta vista maneja la creación de una nueva categoría. En el método `GET`, muestra un formulario vacío para la creación de una nueva categoría. En el método `POST`, procesa la creación de la categoría y valida si se excede el límite de categorías con prioridad.

    :cvar form_class: CategoriaForm - El formulario usado para crear una categoría.
    :cvar template_name: str - Nombre de la plantilla utilizada para el formulario de creación.
    """
    permission_required = 'permissions.crear_categoria'
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


class ModificarCategoriaView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    """
    Vista para modificar una categoría existente.

    Esta vista maneja la modificación de una categoría existente. En el método `GET`, muestra un formulario con los datos de la categoría a modificar. En el método `POST`, procesa la modificación de la categoría y valida si se excede el límite de categorías con prioridad.

    :cvar form_class: CategoriaForm - El formulario usado para modificar una categoría.
    :cvar template_name: str - Nombre de la plantilla utilizada para el formulario de modificación.
    """
    permission_required = 'permissions.modificar_categoria'
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

class EliminarCategoriaView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    """
    Vista para eliminar una categoría existente.

    Esta vista maneja la eliminación de una categoría. Muestra una confirmación en el método `GET` y procesa la eliminación en el método `POST`.

    :cvar template_name: str - Nombre de la plantilla utilizada para confirmar la eliminación.
    """
    permission_required = 'permissions.eliminar_categoria'
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
    Vista para mostrar los detalles de una categoría específica.

    Esta vista maneja la visualización de los detalles de una categoría. En el método `GET`, 
    muestra una plantilla con los detalles de la categoría y los contenidos asociados. 
    En el método `POST`, maneja la creación de una sesión de pago de Stripe para la categoría.

    :cvar model: Categorias - El modelo usado para obtener la categoría.
    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar los detalles de la categoría.
    :cvar context_object_name: str - Nombre del contexto que contiene la categoría.
    """
    model = Categorias
    template_name = 'categories/detalle_categoria.html'
    context_object_name = 'categoria'

    def get_context_data(self, **kwargs):
        """
        Proporciona datos adicionales para la plantilla de detalles de la categoría.

        Incluye todos los contenidos asociados a la categoría específica, el estado del modal
        y la clave pública de Stripe para la integración de pagos.

        :param request: HttpRequest - La solicitud HTTP GET.
        :return: dict - Contexto para la plantilla, incluyendo los contenidos asociados, 
                        el estado del modal y la clave pública de Stripe.
        """
        context = super().get_context_data(**kwargs)

        # Obtener todos los contenidos asociados a esta categoría
        contenidos = Contenido.objects.filter(categoria=self.object, estado='Publicado', activo=True)
        context['contenidos'] = contenidos
        
        if self.request.GET.get('modal') == 'true':
            context['mostrar_modal'] = True
            context['categoria_id'] = self.request.GET.get('categoria_id')
        else:
            context['mostrar_modal'] = False
        context['categorias_restringidas'] = ['GR', 'PA']
        context['STRIPE_PUBLIC_KEY'] = config('STRIPE_PUBLIC_KEY')
            
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud de pago para una categoría específica.

        Crea una sesión de pago de Stripe para la categoría seleccionada, basada en los datos proporcionados en la solicitud.

        :param request: HttpRequest - La solicitud HTTP POST con los datos del pago.
        :param args: list - Lista de argumentos adicionales.
        :param kwargs: dict - Diccionario de parámetros adicionales.
        :return: JsonResponse - Respuesta JSON con el ID de la sesión de Stripe o un mensaje de error en caso de fallo.
        """
        categoria = self.get_object() 
        try:
            # Crear una sesión de pago con Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'pyg',
                            'product_data': {
                                'name': categoria.nombre_categoria,
                            },
                            'unit_amount': categoria.precio,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=self.request.build_absolute_uri('/categorias/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=self.request.build_absolute_uri('/categorias/cancel/'),
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})     


class PaymentSuccessView(View):
    """
    Vista para gestionar el éxito de un pago realizado con Stripe.

    Esta vista maneja la finalización de un pago exitoso. En el método `GET`, 
    verifica la sesión de Stripe y asocia la categoría correspondiente al perfil 
    del usuario autenticado.

    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la confirmación de pago exitoso.
    """
    def get(self, request):
        """
        Verifica la sesión de Stripe y asocia la categoría al perfil del usuario.

        Recupera la sesión de Stripe utilizando el `session_id` proporcionado en la solicitud GET 
        y asocia la categoría correspondiente al perfil del usuario autenticado si la sesión es válida.

        :param request: HttpRequest - La solicitud HTTP GET con el `session_id` de Stripe.
        :return: HttpResponse - Respuesta renderizada con la plantilla de pago completado o redirección a la página principal si no se encuentra el `session_id`.
        """
        session_id = request.GET.get('session_id', None)
        if session_id:
            # Recuperar la sesión de Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            customer_email = session.customer_details.email

            # Recuperar los line items de la sesión
            line_items = stripe.checkout.Session.list_line_items(session_id)
            nombre_categoria = line_items['data'][0]['description']

            # Buscar la categoría basada en la descripción del producto (nombre de la categoría)
            categoria = get_object_or_404(Categorias, nombre_categoria=nombre_categoria)

            # Asociar el usuario a la categoría
            if request.user.is_authenticated:
                request.user.profile.suscripciones.add(categoria)
                request.user.profile.save()

            return render(request, 'categories/pago_completado.html', {'category': categoria})
        return redirect('/')


class PaymentCancelView(View):
    """
    Vista para gestionar la cancelación de un pago con Stripe.

    Esta vista maneja la cancelación de un pago y muestra un mensaje de información
    en la plantilla de cancelación.

    :cvar template_name: str - Nombre de la plantilla utilizada para mostrar la confirmación de pago cancelado.
    """
    def get(self, request):
        """
        Muestra la plantilla de cancelación de pago.

        Renderiza una plantilla que informa al usuario que el pago fue cancelado.

        :param request: HttpRequest - La solicitud HTTP GET.
        :return: HttpResponse - Respuesta renderizada con la plantilla de cancelación de pago.
        """
        return render(request, 'categories/pago_cancelado.html')
