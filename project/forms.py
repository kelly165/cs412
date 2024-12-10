from django import forms  # importing the forms module to create form classes
from .models import ClothingItem, Outfit, Occasion, OutfitItem  # importing the necessary models

# form for creating or editing a clothing item
class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem  # specifying the model for the form
        fields = ['name', 'category', 'color', 'size', 'season', 'image', 'occasions']  # defining which fields to include
        widgets = {
            'season': forms.CheckboxSelectMultiple(),  # allows selecting multiple seasons with checkboxes
            'occasions': forms.CheckboxSelectMultiple(),  # allows selecting multiple occasions with checkboxes
        }

# form for creating or editing an outfit
class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit  # specifying the model for the form
        fields = ['name', 'description']  # defining the fields for the outfit form

# form to filter clothing items based on various criteria
class ClothingItemFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + ClothingItem.CATEGORY_CHOICES,  # category filter with an 'All Categories' option
        required=False  # the field is optional
    )
    color = forms.CharField(max_length=30, required=False, label='Color')  # color filter field, optional
    size = forms.CharField(max_length=10, required=False, label='Size')  # size filter field, optional
    season = forms.MultipleChoiceField(
        choices=ClothingItem.SEASON_CHOICES,  # allows selecting multiple seasons
        required=False,  # the field is optional
        widget=forms.CheckboxSelectMultiple  # uses checkboxes for multiple selection
    )
    occasion = forms.ModelMultipleChoiceField(
        queryset=Occasion.objects.all(),  # allows selecting multiple occasions
        widget=forms.CheckboxSelectMultiple,  # uses checkboxes for multiple selection
        required=False  # the field is optional
    )

# form for editing a clothing item
class EditClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem  # specifying the model for the form
        fields = [
            'name', 'category', 'color',  # fields for clothing item details
            'size', 'season', 'image', 'occasions'  # additional fields like season, image, and occasions
        ]
