from django import forms
from .models import ClothingItem, Outfit, Occasion, OutfitItem


class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ['name', 'category', 'color', 'size', 'season', 'image', 'occasions']
        widgets = {
            'season': forms.CheckboxSelectMultiple(),
            'occasions': forms.CheckboxSelectMultiple(),
        }

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['name', 'description']

class ClothingItemFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + ClothingItem.CATEGORY_CHOICES, 
        required=False
    )
    color = forms.CharField(max_length=30, required=False, label='Color')
    size = forms.CharField(max_length=10, required=False, label='Size')
    season = forms.MultipleChoiceField(
        choices=ClothingItem.SEASON_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    occasion = forms.ModelMultipleChoiceField(
        queryset=Occasion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    
class EditClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = [
            'name', 'category', 'color', 
            'size', 'season', 'image', 'occasions'
        ]