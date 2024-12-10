from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View, DeleteView, UpdateView
from .models import ClothingItem, Outfit, OutfitItem
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView
from .forms import ClothingItemForm, ClothingItemFilterForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.views import LoginView
from .forms import OutfitForm, ClothingItemFilterForm, EditClothingItemForm
import random


# view for user login, specifies the template to use for login
class CustomLoginView(LoginView):
    template_name = 'project/login.html'

    # override to define custom login URL
    def get_login_url(self):
        return '/project/login/'

# view for listing clothing items, restricted to logged-in users
class ClothingItemListView(LoginRequiredMixin, ListView):
    model = ClothingItem
    template_name = 'project/clothingitem_list.html'
    context_object_name = 'clothing_items'

    # filter clothing items to show only those belonging to the logged-in user
    def get_queryset(self):
        return ClothingItem.objects.filter(user=self.request.user)

# view for showing details of a specific clothing item, restricted to logged-in users
class ClothingItemDetailView(LoginRequiredMixin, DetailView):
    model = ClothingItem
    template_name = 'project/clothingitem_detail.html'

# view for listing outfits, restricted to logged-in users
class OutfitListView(LoginRequiredMixin, ListView):
    model = Outfit
    template_name = 'project/outfit_list.html'
    context_object_name = 'outfits'

    # filter outfits to show only those belonging to the logged-in user
    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)

# view for creating a new clothing item, restricted to logged-in users
class ClothingItemCreateView(LoginRequiredMixin, CreateView):
    model = ClothingItem
    form_class = ClothingItemForm
    template_name = 'project/clothingitem_form.html'
    success_url = reverse_lazy('clothing_item_list')

    # set the owner of the clothing item to the logged-in user
    def form_valid(self, form):
        form.instance.user = self.request.user  # set the owner
        return super().form_valid(form)

# view for showing details of a specific outfit, restricted to logged-in users
class OutfitDetailView(LoginRequiredMixin, DetailView):
    model = Outfit
    template_name = 'project/outfit_detail.html'
    context_object_name = 'outfit'

    # add additional context to the template, including associated outfit items
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outfit_items = self.object.outfititem_set.all()  # get all outfit items for the current outfit
        context['outfit_items'] = outfit_items
        return context

# view for user registration
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()  # create an empty registration form
        return render(request, 'project/register.html', {'form': form})

    # handle the registration form submission
    def post(self, request):
        form = UserCreationForm(request.POST)  # create form with submitted data
        if form.is_valid():
            form.save()  # save the new user
            return redirect('login')  # redirect to login after successful registration
        return render(request, 'project/register.html', {'form': form})
    
# home page view, accessible without login
def home(request):
    return render(request, 'project/home.html')

# view for creating an outfit, with an optional clothing item filter
class CreateOutfitView(View):
    def get(self, request):
        outfit_form = OutfitForm()  # create an empty form for creating an outfit
        filter_form = ClothingItemFilterForm()  # create an empty filter form
        clothing_items = ClothingItem.objects.filter(user=request.user)  # get all user's clothing items
        return render(
            request, 
            'project/create_outfit.html', 
            {'outfit_form': outfit_form, 'filter_form': filter_form, 'clothing_items': clothing_items}
        )

    def post(self, request):
        outfit_form = OutfitForm(request.POST)  # create outfit form with submitted data
        filter_form = ClothingItemFilterForm(request.POST)  # create filter form with submitted data

        # if the filter is applied, apply the filtering criteria to the clothing items
        if 'filter' in request.POST:
            clothing_items = ClothingItem.objects.filter(user=request.user)
            if filter_form.is_valid():
                category = filter_form.cleaned_data['category']
                color = filter_form.cleaned_data['color']
                size = filter_form.cleaned_data['size']
                occasions = filter_form.cleaned_data.get('occasion')
                season = filter_form.cleaned_data['season']

                # apply filters based on form input
                if category:
                    clothing_items = clothing_items.filter(category=category)
                if color:
                    clothing_items = clothing_items.filter(color__icontains=color)
                if size:
                    clothing_items = clothing_items.filter(size__icontains=size)
                for selected_season in season:
                    clothing_items = clothing_items.filter(season__contains=selected_season)
                if occasions:
                    clothing_items = clothing_items.filter(occasions__in=occasions).distinct()

            return render(
                request, 
                'project/create_outfit.html', 
                {'outfit_form': outfit_form, 'filter_form': filter_form, 'clothing_items': clothing_items}
            )

        # if the outfit form is valid, create the outfit and associate selected clothing items
        if outfit_form.is_valid():
            outfit = outfit_form.save(commit=False)
            outfit.user = request.user  # assign the current user to the outfit
            outfit.save()

            selected_items = {
                'Top': request.POST.get('top'),
                'Bottom': request.POST.get('bottom'),
                'Shoes': request.POST.get('shoes'),
                'Accessory': request.POST.get('accessory')
            }

            # create OutfitItem for each selected clothing item
            for category, item_id in selected_items.items():
                if item_id:
                    clothing_item = ClothingItem.objects.get(id=item_id)
                    OutfitItem.objects.create(outfit=outfit, clothing_item=clothing_item)

            return redirect('outfit_list')  # redirect to outfit list page after creation

        return render(
            request, 
            'project/create_outfit.html', 
            {'outfit_form': outfit_form, 'filter_form': filter_form, 'clothing_items': ClothingItem.objects.filter(user=request.user)}
        )

# view for generating a random outfit from the user's clothing items
class RandomOutfitView(View):
    def get(self, request):
        # fetch all clothing items by category
        tops = ClothingItem.objects.filter(category='Top', user=request.user)
        bottoms = ClothingItem.objects.filter(category='Bottom', user=request.user)
        shoes = ClothingItem.objects.filter(category='Shoes', user=request.user)
        accessories = ClothingItem.objects.filter(category='Accessory', user=request.user)

        # randomly select items from each category
        outfit = {
            'top': random.choice(tops) if tops.exists() else None,
            'bottom': random.choice(bottoms) if bottoms.exists() else None,
            'shoes': random.choice(shoes) if shoes.exists() else None,
            'accessory': random.choice(accessories) if accessories.exists() else None,
        }

        return render(request, 'project/random_outfit.html', {
            'outfit': outfit
        })

# view for deleting an outfit, restricted to logged-in users
class OutfitDeleteView(LoginRequiredMixin, DeleteView):
    model = Outfit
    template_name = 'project/outfit_confirm_delete.html'
    success_url = reverse_lazy('outfit_list')

    # ensure that the outfit to be deleted belongs to the current user
    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)

# view for editing a clothing item, restricted to logged-in users
class EditClothingItemView(UpdateView):
    model = ClothingItem
    form_class = EditClothingItemForm
    template_name = 'project/edit_clothing_item.html'
    
    # redirect to the detail view of the edited clothing item after successful edit
    def get_success_url(self):
        return reverse_lazy('clothing_item_detail', kwargs={'pk': self.object.pk})

# view for deleting a clothing item, restricted to logged-in users
class DeleteClothingItemView(DeleteView):
    model = ClothingItem
    template_name = 'project/clothingitem_confirm_delete.html'
    success_url = reverse_lazy('clothing_item_list')
