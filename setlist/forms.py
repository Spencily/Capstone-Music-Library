from library.models import Piece
from .models import Setlist
from django import forms


class SetForm(forms.ModelForm):
    pieces = forms.ModelMultipleChoiceField(
        queryset=Piece.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Setlist
        fields = ["title", "description", "pieces"]
