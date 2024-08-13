from .models import Part, Piece
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, BaseInput
from crispy_forms.bootstrap import FieldWithButtons


class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = [
            "title",
            "composer",
            "arranged_by",
            "genre",
            "mc_location",
            "band_arrangement",
        ]


class PartForm(forms.ModelForm):
    pdf_file = forms.FileField(label="Select a file")

    class Meta:
        model = Part
        fields = ["instrument", "part_number", "pdf_file"]


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100, required=False)
    filter = forms.ChoiceField(
        label="Filter",
        choices=[
            ("", "..."),
            ("title", "Title"),
            ("composer", "Composer"),
            ("genre", "Genre"),
            ("band_arrangement", "Band Arrangement"),
        ],
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    FieldWithButtons(
                        "query",
                        SubmitPlain(
                            "submit", "Search", css_class="btn-primary"
                        ),
                    ),
                    css_class="col-8 search",
                ),
                Div(
                    "filter",
                    css_class="col filter",
                ),
                css_class="row search-bar",
            ),
        )


class SubmitPlain(BaseInput):
    input_type = "submit"
    field_classes = "btn"
