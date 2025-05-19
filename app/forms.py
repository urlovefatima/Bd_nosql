from django import forms

class EventForm(forms.Form):
    titre = forms.CharField(max_length=100)
    categorie = forms.CharField(max_length=100)
    localisation = forms.CharField(max_length=100)
    date_heure = forms.DateTimeField(
    input_formats=['%Y-%m-%dT%H:%M'],
    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    capacite = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()