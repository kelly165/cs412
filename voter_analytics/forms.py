# forms.py
from django import forms
from .models import Voter
from datetime import date

class VoterFilterForm(forms.Form):
    # Party affiliation dropdown
    party_affiliation = forms.ChoiceField(
        choices=[('', 'Any')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False,
        label="Party Affiliation"
    )
    
    # Minimum and Maximum Date of Birth dropdowns (years only)
    current_year = date.today().year
    years = [(year, year) for year in range(current_year, current_year - 120, -1)]
    
    min_date_of_birth = forms.ChoiceField(
        choices=[('', 'Any')] + years,
        required=False,
        label="Minimum Year of Birth"
    )
    max_date_of_birth = forms.ChoiceField(
        choices=[('', 'Any')] + years,
        required=False,
        label="Maximum Year of Birth"
    )
    
    # Voter Score dropdown
    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(score, score) for score in Voter.objects.values_list('voter_score', flat=True).distinct()],
        required=False,
        label="Voter Score"
    )

    # Specific elections (checkboxes)
