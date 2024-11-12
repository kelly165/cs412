# views.py
from django.shortcuts import render
from django.views.generic import ListView
from .models import Voter
from .forms import VoterFilterForm
from django.views.generic import DetailView
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
from django.db.models import Count

class GraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Initialize the filter form with GET data (if any)
        filter_form = VoterFilterForm(self.request.GET)
        voters = Voter.objects.all()

        # Apply filters if form is valid
        if filter_form.is_valid():
            if filter_form.cleaned_data.get('party_affiliation'):
                voters = voters.filter(party_affiliation=filter_form.cleaned_data['party_affiliation'])
            if filter_form.cleaned_data.get('min_date_of_birth'):
                voters = voters.filter(date_of_birth__year__gte=filter_form.cleaned_data['min_date_of_birth'])
            if filter_form.cleaned_data.get('max_date_of_birth'):
                voters = voters.filter(date_of_birth__year__lte=filter_form.cleaned_data['max_date_of_birth'])
            if filter_form.cleaned_data.get('voter_score'):
                voters = voters.filter(voter_score=filter_form.cleaned_data['voter_score'])
            if filter_form.cleaned_data.get('elections'):
                for election in filter_form.cleaned_data['elections']:
                    voters = voters.filter(**{election: True})

        # Generate Graphs with the filtered data

        # Graph 1: Distribution by Year of Birth
        birth_year_data = voters.values('date_of_birth__year').annotate(count=Count('id'))
        birth_years = [entry['date_of_birth__year'] for entry in birth_year_data]
        birth_counts = [entry['count'] for entry in birth_year_data]

        fig1 = go.Figure(data=[go.Bar(x=birth_years, y=birth_counts)])
        fig1.update_layout(title="Distribution of Voters by Year of Birth", xaxis_title="Year of Birth", yaxis_title="Count of Voters")
        graph1_div = plot(fig1, output_type="div")

        # Graph 2: Distribution by Party Affiliation
        party_data = voters.values('party_affiliation').annotate(count=Count('party_affiliation'))
        fig2 = go.Figure(data=[go.Pie(labels=[entry['party_affiliation'] for entry in party_data], values=[entry['count'] for entry in party_data])])
        fig2.update_layout(title="Distribution of Voters by Party Affiliation")
        graph2_div = plot(fig2, output_type="div")

        # Graph 3: Participation in Each Election
        elections = ['v20state', 'v21primary', 'v21town', 'v22general', 'v23town']
        election_counts = [voters.filter(**{election: True}).count() for election in elections]
        fig3 = go.Figure(data=[go.Bar(x=elections, y=election_counts)])
        fig3.update_layout(title="Voter Participation in Each Election", xaxis_title="Election", yaxis_title="Number of Participants")
        graph3_div = plot(fig3, output_type="div")

        # Add graphs and form to context
        context['graph1'] = graph1_div
        context['graph2'] = graph2_div
        context['graph3'] = graph3_div
        context['filter_form'] = filter_form
        return context
    
class VoterDetailView(DetailView):
    #View for individual voter
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterListView(ListView):
    # My view for voter list page
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # 100 records per page

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Handle the filtering form submission
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            # Filter by party affiliation
            party_affiliation = form.cleaned_data.get('party_affiliation')
            if party_affiliation:
                queryset = queryset.filter(party_affiliation=party_affiliation)

            # Filter by date of birth range
            min_date_of_birth = form.cleaned_data.get('min_date_of_birth')
            max_date_of_birth = form.cleaned_data.get('max_date_of_birth')
            if min_date_of_birth:
                queryset = queryset.filter(date_of_birth__year__gte=min_date_of_birth)
            if max_date_of_birth:
                queryset = queryset.filter(date_of_birth__year__lte=max_date_of_birth)

            # Filter by voter score
            voter_score = form.cleaned_data.get('voter_score')
            if voter_score:
                queryset = queryset.filter(voter_score=voter_score)

            # Filter by elections (checkboxes)
            elections = form.cleaned_data.get('elections')
            if elections:
                for election in elections:
                    queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the filter form to the context so it can be used in the template
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context
