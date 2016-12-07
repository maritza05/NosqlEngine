from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    min_rank = forms.IntegerField(required=False, label="Minimum Rank")
    max_rank = forms.IntegerField(required=False, label="Maximum Rank")


