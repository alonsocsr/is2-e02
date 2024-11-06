from collections import defaultdict
from django.views.generic import FormView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import requests
from django.db.models import Sum
from .forms import ProfileForm, ConfirmDeleteAccountForm
from .models import Profile, Suscripcion
from django.contrib import messages
from django.contrib.auth import logout
from categories.models import Categorias
from content.models import Contenido
from django.shortcuts import get_list_or_404, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import ListView
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, time, timedelta
from django.utils import timezone
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef

class UpdateProfile(LoginRequiredMixin, FormView, PermissionRequiredMixin):
    """
    La clase `UpdateProfile` define la vista para actualizar el perfil del usuario actual.

    Esta vista utiliza un formulario para permitir que los usuarios autenticados 
    modifiquen su información personal, como nombre, apellido, nombre de usuario y foto de perfil.

    :cvar template_name: str - Nombre de la plantilla utilizada para el formulario de actualización del perfil.
    :cvar permission_required: str - Permiso necesario para acceder a esta vista.
    :cvar form_class: ProfileForm - El formulario utilizado para actualizar el perfil.
    
    """
    template_name = "profiles/profile.html"
    permission_required = 'permissions.editar_perfil'

    form_class = ProfileForm

    def get_initial(self):
        """
        Inicializa los valores del formulario con la información actual del usuario.  

        :return: dict - Un diccionario con los datos iniciales para el formulario.
        """
        initial = super().get_initial()
        user = self.request.user
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['username'] = user.username
        # initial['image'] = user.profile.image
        return initial

    def form_valid(self, form):
        """
        Procesa los datos cuando el formulario es valido.

        Actualiza el perfil del usuario con los nuevos datos proporcionados en el formulario.
        Muestra un mensaje de éxito al usuario.

        :param form: ProfileForm - El formulario validado.  

        :return: HttpResponseRedirect - Redirige a la URL de éxito.
        """
        user = self.request.user
        profile = Profile.objects.get(user=user)

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        if form.cleaned_data['username'] is not None:
            user.username = form.cleaned_data['username']

        if form.cleaned_data['image'] is not None:
            profile.image = form.cleaned_data['image']
            profile.save()

        user.save()
        messages.success(self.request, "Perfil actualizado con éxito.")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Define la URL de redirección después de que el formulario se haya procesado correctamente.  

        :return: str - La URL a la que se redirige al usuario.
        """
        return self.request.path
    
    def get_context_data(self, **kwargs):
        """
        Añade los roles del usuario al contexto para ser utilizados en el template.

        :param \**kwargs: Parámetros adicionales que se pasan al método.  

        :return: dict - Contexto actualizado con la información de los roles del usuario.
        """
        context = super().get_context_data(**kwargs)
        # Suponiendo que tienes una relación entre el usuario y los roles
        user = self.request.user
        context['user_roles'] = user.groups.all()  # Asumiendo que estás utilizando grupos para roles
        return context


@login_required
def categoria_interes(request, categoria_id):
    """
    Maneja el interés de un usuario en una categoría.

    Permite agregar o quitar una categoría de la lista de intereses del usuario. 

    :param request: HttpRequest - La solicitud HTTP POST.
    :param categoria_id: int - El ID de la categoría a modificar.  

    :return: JsonResponse - Respuesta en formato JSON indicando si la categoría está en los intereses o no.
    """
    if request.method == 'POST':
        categoria = get_object_or_404(Categorias, id=categoria_id)
        profile = request.user.profile 

        if categoria in profile.categorias_interes.all():
            profile.categorias_interes.remove(categoria)
            is_interes = False
        else:
            profile.categorias_interes.add(categoria)
            is_interes = True

    
        return JsonResponse({
            'success': True,
            'is_interes': is_interes,
        })

    return JsonResponse({'success': False, 'error': 'Request invalidop.'})


@login_required
def registrar_suscripcion(request, categoria_id):
    """
    Registra una suscripción de un usuario a una categoría paga.

    :param request: HttpRequest - La solicitud HTTP POST.
    :param categoria_id: int - El ID de la categoría a la que se quiere suscribir.  

    :return: HttpResponseRedirect - Redirige al usuario a la página de detalle de la categoría.
    """
    categoria = get_object_or_404(Categorias, id=categoria_id)
    
    perfil = request.user.profile
    perfil.suscripciones.add(categoria)
    return redirect('categories:detalle', pk=categoria_id)

class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        """
        Maneja la acción de dar like a un contenido.

        Permite al usuario dar o quitar un like al contenido.

        :param request: HttpRequest - La solicitud HTTP POST.
        :param args: list - Argumentos adicionales para la vista.
        :param kwargs: dict - Argumentos de palabra clave adicionales para la vista.  

        :cvar contenido_id: int - El ID del contenido que se está procesando.
        :cvar content: Contenido - El contenido al que se le da like.
        :cvar profile: Profile - El perfil del usuario actual.

        :return: JsonResponse - Respuesta en formato JSON con el estado del like y conteos.
        """
        contenido_id = self.kwargs.get('id')
        content = get_object_or_404(Contenido, id=contenido_id)
        profile = request.user.profile

        liked = content in profile.contenidos_like.all()
        disliked = content in profile.contenidos_dislike.all()

        if liked:
            profile.contenidos_like.remove(content)  # Si ya tenía like, quitar
            content.cantidad_likes -= 1
        else:
            profile.contenidos_like.add(content)  # Si no tenía like, agregar
            content.cantidad_likes += 1
            if disliked:
                profile.contenidos_dislike.remove(content)  # Si tenía dislike, quitar
                content.cantidad_dislikes -= 1

        content.save()

        return JsonResponse({
            'success': True,
            'liked': content in profile.contenidos_like.all(),
            'disliked': content in profile.contenidos_dislike.all(),
            'like_count': content.cantidad_likes,
            'dislike_count': content.cantidad_dislikes
        })

class DislikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        """
        Maneja la acción de dar dislike a un contenido.

        Permite al usuario dar o quitar un dislike al contenido.

        :param request: HttpRequest - La solicitud HTTP POST.
        :param args: list - Argumentos adicionales para la vista.
        :param kwargs: dict - Argumentos de palabra clave adicionales para la vista.
        
        :cvar contenido_id: int - El ID del contenido que se está procesando.
        :cvar content: Contenido - El contenido al que se le da dislike.
        :cvar profile: Profile - El perfil del usuario actual.

        :return: JsonResponse - Respuesta en formato JSON con el estado del dislike y conteos.
        """
        contenido_id = self.kwargs.get('id')
        content = get_object_or_404(Contenido, id=contenido_id)
        profile = request.user.profile  

        liked = content in profile.contenidos_like.all()
        disliked = content in profile.contenidos_dislike.all()

        if disliked:
            profile.contenidos_dislike.remove(content)  # Si ya tenía dislike, quitar
            content.cantidad_dislikes -= 1
        else:
            profile.contenidos_dislike.add(content)  # Si no tenía dislike, agregar
            content.cantidad_dislikes += 1
            if liked:
                profile.contenidos_like.remove(content)  # Si tenía like, quitar
                content.cantidad_likes -= 1

        content.save()

        return JsonResponse({
            'success': True,
            'liked': content in profile.contenidos_like.all(),
            'disliked': content in profile.contenidos_dislike.all(),
            'like_count': content.cantidad_likes,
            'dislike_count': content.cantidad_dislikes
        })
    

class EliminarCuentaView(LoginRequiredMixin, FormView):
    """
    Vista para eliminar la cuenta del usuario y su perfil asociado.

    Requiere que el usuario esté autenticado y proporciona un formulario para que el usuario confirme la eliminación de su cuenta mediante la 
    verificación de su contraseña.

    :cvar form_class: ConfirmDeleteAccountForm - Clase de formulario utilizada para validar la contraseña antes de 
    eliminar la cuenta.
    :cvar success_url: str - URL a la que se redirige al usuario después de que se haya eliminado 
    exitosamente su cuenta.
    """

    form_class = ConfirmDeleteAccountForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Valida el formulario y elimina la cuenta del usuario.

        Desconecta al usuario después de eliminar la cuenta y muestra un mensaje de éxito.

        :param form: ConfirmDeleteAccountForm - El formulario validado.

        :return: HttpResponseRedirect - Redirige al usuario a la URL de éxito.
        """
        user = self.request.user
        password = form.cleaned_data.get('password')
        
        # Verificar la contraseña del usuario
        if not user.check_password(password):
            form.add_error('password', 'La contraseña es incorrecta.')
            return self.form_invalid(form)

        # Eliminar perfil si existe
        try:
            profile = Profile.objects.get(user=user)
            profile.delete()
        except Profile.DoesNotExist:
            pass

        # Eliminar el usuario
        user.delete()
        logout(self.request)
        messages.success(self.request, 'Tu cuenta ha sido eliminada exitosamente.')
        return super().form_valid(form)
    

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    
class VerHistorialCompras(LoginRequiredMixin,ListView):

    """
    Vista para mostrar el historial de compras o suscripciones registradas en el sistema.

    Muestra los registros de cambios de estado realizados por el usuario.

    :cvar model: Modelo utilizado para almacenar los cambios de estado.
    :cvar template_name: str - Nombre de la plantilla utilizada para renderizar la lista de cambios.
    :cvar context_object_name: str - Nombre del contexto para la lista de cambios.
    :cvar permission_required: str - Permiso requerido para acceder a esta vista.
    :cvar paginate_by: int - Número de registros por página para la paginación.
    """
    model = Profile
    template_name = 'profiles/ver_historial_pagos.html'
    context_object_name = 'historial_pagos'
    #permission_required= 'permissions.ver_historial_compras'

    def get_queryset(self):
    
        user = self.request.user
        
        if user.groups.filter(name="Financiero").exists():
            queryset = Suscripcion.objects.all() 
        else:
            queryset = Suscripcion.objects.filter(profile=user.profile)

        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__id=categoria)
        
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')

        if fecha_desde and fecha_hasta:
            fecha_desde = parse_date(fecha_desde)
            fecha_hasta = parse_date(fecha_hasta)
            if fecha_desde <= fecha_hasta: 
                fecha_hasta = datetime.combine(fecha_hasta, time.max)
                fecha_hasta = make_aware(fecha_hasta)
                queryset = queryset.filter(fecha_pago__range=(fecha_desde, fecha_hasta))
        
        # Filtro de usuario
        usuario_id = self.request.GET.get('usuario')
        if usuario_id:
            queryset = queryset.filter(profile__user__id=usuario_id)
        
        return queryset.order_by("fecha_pago")         
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_suscr'] = self.request.user.is_authenticated and self.request.user.groups.filter(name="Suscriptor").exists()
        context['is_fin'] = self.request.user.is_authenticated and self.request.user.groups.filter(name="Financiero").exists()
        context['categorias'] = Categorias.objects.filter(tipo_categoria='PA')  
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')  

        # Obtener solo los usuarios con suscripciones
        usuarios_con_suscripcion = User.objects.filter(
            Exists(Suscripcion.objects.filter(profile__user=OuterRef('pk')))
        )
        context['usuarios'] = usuarios_con_suscripcion
        context['usuario_seleccionado'] = self.request.GET.get('usuario', '')

        categoria = self.request.GET.get('categoria', None)
        usuario = self.request.GET.get('usuario', None)


        fecha_desde = self.request.GET.get('fecha_desde', None)
        fecha_hasta = self.request.GET.get('fecha_hasta', None)
        context['fecha_desde'] = fecha_desde
        context['fecha_hasta'] = fecha_hasta
        
        total_general = self.get_queryset().aggregate(Sum('monto'))['monto__sum'] or 0
        
        context['total_general'] = total_general

        if fecha_desde and fecha_hasta:
            fecha_desde = parse_date(fecha_desde)
            fecha_hasta = parse_date(fecha_hasta)

            if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
                messages.error(self.request, "La fecha 'desde' no puede ser mayor que la fecha 'hasta'.", extra_tags="fecha_error")
                return context
            else:
                fecha_hasta = make_aware(datetime.combine(fecha_hasta, time.max))
            
        totales_categoria=self.grafico_totales_categoria(fecha_desde, fecha_hasta, categoria, usuario)
        reporte_pagos=self.grafico_montos_pago_por_fecha(fecha_desde, fecha_hasta, categoria, usuario)
        reportes_categoria=self.grafico_datos_montos_por_categoria(fecha_desde, fecha_hasta, categoria, usuario)
        context['grafico1']=totales_categoria
        context['montos_fecha']=reporte_pagos
        context['montos_categoria']=reportes_categoria
        return context

    def grafico_totales_categoria(self, start_date=None, end_date=None, categoria=None, usuario=None):
        suscripciones = Suscripcion.objects.all()
        if categoria:
            suscripciones = suscripciones.filter(categoria__id=categoria)

        if usuario:
            suscripciones = suscripciones.filter(profile__user__id=usuario)
        
        if start_date and end_date:
            suscripciones = suscripciones.filter(fecha_pago__range=(start_date, end_date))
        else:
            today = timezone.now().date()
            suscripciones = suscripciones.filter(fecha_pago__range=(today - timedelta(days=7), today))
        
        suscripcion_by_category = defaultdict(lambda: {'cantidad': 0})
        for susc in suscripciones:
            category = susc.categoria.nombre_categoria
            suscripcion_by_category[category]['cantidad'] += 1
        
    
        categorias = list(suscripcion_by_category.keys())
        cantidades = [data['cantidad'] for data in suscripcion_by_category.values()]
        

        return {
            'labels': categorias,
            'series': cantidades
        }
        
    def grafico_montos_pago_por_fecha(self, start_date=None, end_date=None, categoria=None, usuario=None):
        
        if not start_date or not end_date:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)

        pagos_por_categoria = (
            Suscripcion.objects
            .filter(fecha_pago__range=(start_date, end_date))
            .values("fecha_pago__date")
            .annotate(total_monto=Sum("monto"))
            .order_by("-fecha_pago__date")
        )
        if categoria:
            pagos_por_categoria = pagos_por_categoria.filter(categoria__id=categoria)
        
        if usuario:
            pagos_por_categoria = pagos_por_categoria.filter(profile__user__id=usuario)
        fechas = []
        montos=[]
     
        for entry in pagos_por_categoria:
            monto = entry["total_monto"]
            fecha = entry["fecha_pago__date"].strftime('%d %b') 
            
            fechas.append(fecha)
            montos.append(monto)
        return {
            "fechas":fechas,
            "montos":montos
        }
        
    
            
    def grafico_datos_montos_por_categoria(self,start_date=None, end_date=None, categoria=None, usuario=None):
        if not start_date or not end_date:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)

        pagos_por_fecha_categoria = (
            Suscripcion.objects
            .filter(fecha_pago__range=(start_date, end_date))
            .values("fecha_pago__date", "categoria__nombre_categoria")
            .annotate(total_monto=Sum("monto"))
            .order_by("-fecha_pago__date")
        )
        if categoria:
            pagos_por_fecha_categoria = pagos_por_fecha_categoria.filter(categoria__id=categoria)

        if usuario:
            pagos_por_fecha_categoria = pagos_por_fecha_categoria.filter(profile__user__id=usuario)

        fechas = set()
        categorias_montos = defaultdict(lambda: [])

        for entry in pagos_por_fecha_categoria:
            fecha = entry["fecha_pago__date"].strftime('%d %b')
            categoria = entry["categoria__nombre_categoria"]
            monto = entry["total_monto"]

            fechas.add(fecha)
            categorias_montos[categoria].append((fecha, monto))

        fechas = sorted(fechas,reverse=True)  
        series = []
        for categoria, data in categorias_montos.items():
            montos = [next((m for f, m in data if f == fecha), 0) for fecha in fechas]
            series.append({
                "name": categoria,
                "data": montos,
            })

        return {
            "fechas": fechas,
            "series": series,
        }

def exportar_compras_xlsx(request):
    # Crear el archivo Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Historial de Compras'

    # Agregar encabezados
    headers = ['Usuario', 'Categoría', 'Fecha del Pago', 'Hora del Pago', 'Monto', 'Medio de Pago']
    sheet.append(headers)

    # Obtener queryset filtrado (reutilizando la lógica de get_queryset)
    user = request.user
    if user.groups.filter(name="Financiero").exists():
        queryset = Suscripcion.objects.all()
    else:
        queryset = Suscripcion.objects.filter(profile=user.profile)

    # Aplicar filtros
    categoria = request.GET.get('categoria')
    if categoria:
        queryset = queryset.filter(categoria__id=categoria)

    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    if fecha_desde and fecha_hasta:
        fecha_desde = parse_date(fecha_desde)
        fecha_hasta = parse_date(fecha_hasta)
        if fecha_desde <= fecha_hasta:
            fecha_hasta = datetime.combine(fecha_hasta, time.max)
            fecha_hasta = make_aware(fecha_hasta)
            queryset = queryset.filter(fecha_pago__range=(fecha_desde, fecha_hasta))

    # Agregar los datos a la hoja de Excel
    for compra in queryset:
        row = [
            compra.profile.user.username,
            compra.categoria.nombre_categoria,
            compra.fecha_pago.strftime("%Y-%m-%d"),
            compra.fecha_pago.strftime("%H:%M"),
            compra.monto,
            compra.medio_pago
        ]
        sheet.append(row)

    # Configurar la respuesta para descargar el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=historial_compras.xlsx'
    workbook.save(response)
    return response
