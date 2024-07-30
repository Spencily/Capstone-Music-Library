from .models import Piece
from django import forms

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['title', 'composer', 'arranged_by', 'genre', 'mc_location', 'band_arrangement']