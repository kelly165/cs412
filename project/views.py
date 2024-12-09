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
from .forms import OutfitForm, ClothingItemFilterForm
import random




class CustomLoginView(LoginView):
    template_name = 'project/login.html'

    def get_login_url(self):
        return '/project/login/'

class ClothingItemListView(LoginRequiredMixin, ListView):
    model = ClothingItem
    template_name = 'project/clothingitem_list.html'
    context_object_name = 'clothing_items'

    def get_queryset(self):
        return ClothingItem.objects.filter(user=self.request.user)

class ClothingItemDetailView(LoginRequiredMixin, DetailView):
    model = ClothingItem
    template_name = 'project/clothingitem_detail.html'

class OutfitListView(LoginRequiredMixin, ListView):
    model = Outfit
    template_name = 'project/outfit_list.html'
    context_object_name = 'outfits'

    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)



class ClothingItemCreateView(LoginRequiredMixin, CreateView):
    model = ClothingItem
    form_class = ClothingItemForm
    template_name = 'project/clothingitem_form.html'
    success_url = reverse_lazy('clothing_item_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the owner
        return super().form_valid(form)

class OutfitDetailView(LoginRequiredMixin, DetailView):
    model = Outfit
    template_name = 'project/outfit_detail.html'
    context_object_name = 'outfit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all the OutfitItems for the current outfit and their associated clothing items
        outfit_items = self.object.outfititem_set.all()
        context['outfit_items'] = outfit_items
        return context

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'project/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
        return render(request, 'project/register.html', {'form': form})
    

def home(request):
    return render(request, 'project/home.html')



class CreateOutfitView(View):
    def get(self, request):
        outfit_form = OutfitForm()
        filter_form = ClothingItemFilterForm()
        clothing_items = ClothingItem.objects.filter(user=request.user)
        return render(
            request, 
            'project/create_outfit.html', 
            {'outfit_form': outfit_form, 'filter_form': filter_form, 'clothing_items': clothing_items}
        )

    def post(self, request):
        outfit_form = OutfitForm(request.POST)
        filter_form = ClothingItemFilterForm(request.POST)

        if 'filter' in request.POST:
            clothing_items = ClothingItem.objects.filter(user=request.user)
            if filter_form.is_valid():
                category = filter_form.cleaned_data['category']
                color = filter_form.cleaned_data['color']
                size = filter_form.cleaned_data['size']
                occasions = filter_form.cleaned_data.get('occasion')

                season = filter_form.cleaned_data['season']

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

        if outfit_form.is_valid():
            outfit = outfit_form.save(commit=False)
            outfit.user = request.user
            outfit.save()

            selected_items = {
                'Top': request.POST.get('top'),
                'Bottom': request.POST.get('bottom'),
                'Shoes': request.POST.get('shoes'),
                'Accessory': request.POST.get('accessory')
            }

            for category, item_id in selected_items.items():
                if item_id:
                    clothing_item = ClothingItem.objects.get(id=item_id)
                    OutfitItem.objects.create(outfit=outfit, clothing_item=clothing_item)

            return redirect('outfit_list')  # Redirect to an outfit list page

        return render(
            request, 
            'project/create_outfit.html', 
            {'outfit_form': outfit_form, 'filter_form': filter_form, 'clothing_items': ClothingItem.objects.filter(user=request.user)}
        )
    

class RandomOutfitView(View):
    def get(self, request):
        # Fetch all clothing items from the database
        tops = ClothingItem.objects.filter(category='Top', user=request.user)
        bottoms = ClothingItem.objects.filter(category='Bottom', user=request.user)
        shoes = ClothingItem.objects.filter(category='Shoes', user=request.user)
        accessories = ClothingItem.objects.filter(category='Accessory', user=request.user)

        # Randomly select items from each category
        outfit = {
            'top': random.choice(tops) if tops.exists() else None,
            'bottom': random.choice(bottoms) if bottoms.exists() else None,
            'shoes': random.choice(shoes) if shoes.exists() else None,
            'accessory': random.choice(accessories) if accessories.exists() else None,
        }

        return render(request, 'project/random_outfit.html', {
            'outfit': outfit
        })
    
class OutfitDeleteView(LoginRequiredMixin, DeleteView):
    model = Outfit
    template_name = 'project/outfit_confirm_delete.html'
    success_url = reverse_lazy('outfit_list')

    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)
    

