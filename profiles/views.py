from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileForm
from .models import Profile
   
   
class UpdateProfile(LoginRequiredMixin, FormView):
  template_name = "profiles/profile.html"
  form_class = ProfileForm

  def form_valid(self, form):
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
      
      return super().form_valid(form)
  
  def get_success_url(self):
     return self.request.path
