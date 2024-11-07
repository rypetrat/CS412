from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django import forms
import plotly 
import plotly.graph_objects as go
from django.db.models import Count

class VoterFilterForm(forms.Form):
    # Filter by party affiliation
    PARTY_CHOICES = Voter.objects.values_list('party_affiliation', 'party_affiliation').distinct()
    party_affiliation = forms.ChoiceField(choices=[('', 'Any')] + list(PARTY_CHOICES), required=False, label="Party Affiliation")

    # Filter by date of birth range
    YEARS = [(year, year) for year in range(1900, 2024)]
    min_date_of_birth = forms.ChoiceField(choices=[('', 'Any')] + YEARS, required=False, label="Born After")
    max_date_of_birth = forms.ChoiceField(choices=[('', 'Any')] + YEARS, required=False, label="Born Before")

    # Filter by voter score
    VOTER_SCORE_CHOICES = [(i, i) for i in range(6)]
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + VOTER_SCORE_CHOICES, required=False, label="Voter Score")

    # Filter by specific elections
    v20state = forms.BooleanField(required=False, label="Voted in 2020 State Election")
    v21town = forms.BooleanField(required=False, label="Voted in 2021 Town Election")
    v21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary Election")
    v22general = forms.BooleanField(required=False, label="Voted in 2022 General Election")
    v23town = forms.BooleanField(required=False, label="Voted in 2023 Town Election")

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 50

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            # Apply filters if provided
            party = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_date_of_birth')
            max_dob = form.cleaned_data.get('max_date_of_birth')
            voter_score = form.cleaned_data.get('voter_score')
            v20state = form.cleaned_data.get('v20state')
            v21town = form.cleaned_data.get('v21town')
            v21primary = form.cleaned_data.get('v21primary')
            v22general = form.cleaned_data.get('v22general')
            v23town = form.cleaned_data.get('v23town')

            # Filter by party affiliation
            if party:
                queryset = queryset.filter(party_affiliation=party)
            # Filter by date of birth range
            if min_dob:
                queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
            if max_dob:
                queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
            # Filter by election participation
            if v20state:
                queryset = queryset.filter(v20state=True)
            if v21town:
                queryset = queryset.filter(v21town=True)
            if v21primary:
                queryset = queryset.filter(v21primary=True)
            if v22general:
                queryset = queryset.filter(v22general=True)
            if v23town:
                queryset = queryset.filter(v23town=True)

            if voter_score:
                queryset = [v for v in queryset if v.voter_score == int(voter_score)]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET or None)
        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            # Apply filters if provided
            party = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_date_of_birth')
            max_dob = form.cleaned_data.get('max_date_of_birth')
            v20state = form.cleaned_data.get('v20state')
            v21town = form.cleaned_data.get('v21town')
            v21primary = form.cleaned_data.get('v21primary')
            v22general = form.cleaned_data.get('v22general')
            v23town = form.cleaned_data.get('v23town')

            # Filter by party affiliation
            if party:
                queryset = queryset.filter(party_affiliation=party)
            # Filter by date of birth range
            if min_dob:
                queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
            if max_dob:
                queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
            # Filter by election participation
            if v20state:
                queryset = queryset.filter(v20state=True)
            if v21town:
                queryset = queryset.filter(v21town=True)
            if v21primary:
                queryset = queryset.filter(v21primary=True)
            if v22general:
                queryset = queryset.filter(v22general=True)
            if v23town:
                queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Instantiate the filter form to pass it to the template
        context['form'] = VoterFilterForm(self.request.GET or None)

        # Generate the graphs based on the filtered queryset
        # 1. Histogram: Voter Birth Year Distribution
        birth_years = self.get_queryset().values('date_of_birth__year').annotate(count=Count('id')).order_by('date_of_birth__year')
        birth_year_labels = [entry['date_of_birth__year'] for entry in birth_years]
        birth_year_values = [entry['count'] for entry in birth_years]

        birth_year_fig = go.Figure(data=[
            go.Bar(
                x=birth_year_labels,
                y=birth_year_values,
                marker=dict(color='royalblue')
            )
        ])
        birth_year_fig.update_layout(
            title="Voter Birth Year Distribution",
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters",
            template="plotly_dark"
        )
        
        context['birth_year_graph'] = birth_year_fig.to_html(full_html=False)

        # 2. Pie Chart: Voter Party Affiliation Distribution
        party_counts = self.get_queryset().values('party_affiliation').annotate(count=Count('id')).order_by('party_affiliation')
        party_labels = [entry['party_affiliation'] for entry in party_counts]
        party_values = [entry['count'] for entry in party_counts]

        party_fig = go.Figure(data=[
            go.Pie(
                labels=party_labels,
                values=party_values,
                hole=0.3, 
                marker=dict(colors=['gold', 'lightcoral', 'lightgreen', 'lightskyblue', 'orange'])
            )
        ])
        party_fig.update_layout(
            title="Voter Party Affiliation Distribution",
            template="plotly_dark"
        )
        
        context['party_graph'] = party_fig.to_html(full_html=False)

        # 3. Histogram: Voter Participation in Elections
        election_participation_counts = {
            '2020 State': self.get_queryset().filter(v20state=True).count(),
            '2021 Town': self.get_queryset().filter(v21town=True).count(),
            '2021 Primary': self.get_queryset().filter(v21primary=True).count(),
            '2022 General': self.get_queryset().filter(v22general=True).count(),
            '2023 Town': self.get_queryset().filter(v23town=True).count()
        }

        election_labels = list(election_participation_counts.keys())
        election_values = list(election_participation_counts.values())

        participation_fig = go.Figure(data=[
            go.Bar(
                x=election_labels,
                y=election_values,
                marker=dict(color='lightcoral')
            )
        ])
        participation_fig.update_layout(
            title="Voter Participation in Elections",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
            template="plotly_dark"
        )

        context['participation_graph'] = participation_fig.to_html(full_html=False)

        return context

