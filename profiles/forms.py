from django import forms

class ProfileForm(forms.Form):
  first_name = forms.CharField(
    max_length=150,
    label= 'Nombres'
  )
  last_name = forms.CharField(
    max_length=150,
    label= 'Apellidos'
  )
  username = forms.CharField(
    max_length=150,
    label= 'Nombre de usuario',
    required=False
  )
  image = forms.ImageField(
    label= 'Foto de Perfil',
    required=False
  )

class ConfirmDeleteAccountForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput, label="Confirma tu contraseña")