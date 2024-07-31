from .models import Setlist
from django import forms

class SetForm(forms.ModelForm):
    class Meta:
        model = Setlist
        fields = ['title', 'description', 'pieces']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        setlist = super().save(commit=False)
        if self.user:
            setlist.created_by = self.user
        if commit:
            setlist.save()
        return setlist