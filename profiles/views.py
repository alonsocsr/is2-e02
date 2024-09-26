from django.views.generic import FormView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ProfileForm, ConfirmDeleteAccountForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth import logout
from categories.models import Categorias
from content.models import Contenido
from django.shortcuts import reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm


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
    if request.method == "POST" and request.user.is_authenticated:
        categoria = get_object_or_404(Categorias, id=categoria_id)
        user_profile = request.user.profile  # Asumiendo que hay un perfil de usuario relacionado
        if categoria in user_profile.categorias_interes.all():
            user_profile.categorias_interes.remove(categoria)
            is_interes = False
        else:
            user_profile.categorias_interes.add(categoria)
            is_interes = True

        return JsonResponse({'is_interes': is_interes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

    Requiere que el usuario esté autenticado y proporciona un formulario
    para que el usuario confirme la eliminación de su cuenta mediante la 
    verificación de su contraseña.

    Attributes
    ----------
    form_class : ConfirmDeleteAccountForm
        Clase de formulario utilizada para validar la contraseña antes de 
        eliminar la cuenta.
    success_url : str
        URL a la que se redirige al usuario después de que se haya eliminado 
        exitosamente su cuenta.
    """

    form_class = ConfirmDeleteAccountForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Valida el formulario y elimina la cuenta del usuario si la contraseña 
        proporcionada es correcta.

        Parameters
        ----------
        form : ConfirmDeleteAccountForm
            Instancia del formulario con los datos proporcionados por el usuario.

        Returns
        -------
        HttpResponse
            Respuesta HTTP que redirige a la URL de éxito si la cuenta fue 
            eliminada correctamente. En caso contrario, muestra el formulario 
            con errores.
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
        """
        Retorna una instancia del formulario de eliminación de cuenta.

        Parameters
        ----------
        form_class : ConfirmDeleteAccountForm, optional
            Clase del formulario a utilizar. Si no se proporciona, se usa la 
            clase especificada en `form_class`.

        Returns
        -------
        ConfirmDeleteAccountForm
            Instancia del formulario inicializada con los datos proporcionados.
        """
        form = super().get_form(form_class)
        return form