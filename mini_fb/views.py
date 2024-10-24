from django.shortcuts import render
from .models import StatusMessage, Image
from .forms import CreateStatusMessageForm, UpdateProfileForm

# Create your views here.
from django.views.generic import ListView
from .models import Profile
from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import CreateProfileForm

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    
    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html' 
    context_object_name = 'status_message'

    def get_success_url(self):
        # Get the profile associated with the status message
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'  # Template

    def get_success_url(self):
        #redirect to the profile page
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})

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
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the profile based on the primary key from the URL
        profile_pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=profile_pk)
        return context

    def form_valid(self, form):
        # Get the profile based on the primary key from the URL
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        # Set the profile for the status message
        form.instance.profile = profile
        
        # Save the status message to database
        sm = form.save()
        
        # Process uploaded images
        files = self.request.FILES.getlist('files')
        for file in files:
            # Create an Image object for each uploaded file
            image = Image(image_file=file, status_message=sm)
            image.save()  # Save the Image object to the database
        
        return super().form_valid(form)

    def get_success_url(self):
        # Return the URL to the profile page
        return reverse_lazy('show_profile', kwargs={'pk': self.kwargs['pk']})