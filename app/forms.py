from django import forms

class EventForm(forms.Form):
    titre = forms.CharField(max_length=100)
    categorie = forms.CharField(max_length=100)
    prix = forms.IntegerField(
        required=False, 
        label="Prix (FCFA)",
        widget=forms.TextInput(attrs={
            'placeholder': '0',
            'class': 'form-control'
        })
    )
    STATUT_CHOICES = [
        ('gratuit', 'Gratuit'),
        ('payant', 'Payant'),
    ]

    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        widget=forms.RadioSelect,  
        label="Statut"
    )
    localisation = forms.CharField(max_length=100)
    date_heure = forms.DateTimeField(
    input_formats=['%Y-%m-%dT%H:%M'],
    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    capacite = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()