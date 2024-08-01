from .models import Part, Piece
from django import forms
from cloudinary.forms import CloudinaryFileField

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['title', 'composer', 'arranged_by', 'genre', 'mc_location', 'band_arrangement']


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['instrument', 'part_number', 'pdf_file']
        pdf_file = CloudinaryFileField