from django.shortcuts import render
from .models import StatusMessage
from .forms import CreateStatusMessageForm

# Create your views here.
from django.views.generic import ListView
from .models import Profile
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreateProfileForm



class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add status messages to the context
        context['status_messages'] = self.object.get_status_messages()
        return context
    
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    success_url = reverse_lazy('show_all_profiles') 

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_message_form.html'  # Template for the form

    def form_valid(self, form):
        form.instance.profile = self.get_profile()  # Set the profile for this status message
        return super().form_valid(form)

    def get_profile(self):
        # Logic to get the profile from the URL or session
        # Assuming you pass profile_pk in the URL
        return Profile.objects.get(pk=self.kwargs['profile_pk'])

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})  # Redirect back to the profile