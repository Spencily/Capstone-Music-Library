from .models import Setlist
from django import forms

class SetForm(forms.ModelForm):
    class Meta:
        model = Setlist
        fields = ['title', 'description', 'pieces']