from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import PieceForm, PartForm, SearchForm


class TestPieceForm(TestCase):

    """Tests to see if the piece form is valid"""
    def test_form_is_valid(self):
        piece_form = PieceForm(
            {
                "title": "Test Title",
                "composer": "Test Composer",
                "arranged_by": "Test Arranger",
                "genre": "Test Genre",
                "mc_location": "Test Location",
                "band_arrangement": "Flexi-band",
            }
        )
        self.assertTrue(piece_form.is_valid(), "Form is not valid")

    """Tests to see if the form is invalid through missing fields"""
    def test_form_missing_fields(self):
        piece_form = PieceForm({})
        self.assertFormError(piece_form, "title", "This field is required.")
        self.assertFormError(piece_form, "genre", "This field is required.")
        self.assertFormError(piece_form, "band_arrangement", "This field is required.")

        self.assertFalse(piece_form.is_valid(), "Form is valid")


class TestPartForm(TestCase):
    """Tests to see if the part form is valid"""
    def test_form_is_valid(self):
        file_data = {
            "pdf_file": SimpleUploadedFile(
                "test.pdf", b"file_content", content_type="application/pdf"
            )
        }
        post_data = {
            "instrument": "Test Instrument",
            "part_number": 1,
        }

        part_form = PartForm(data=post_data, files=file_data)
        print(part_form.errors)
        self.assertTrue(part_form.is_valid(), "Form is not valid")

    """Tests to see if the form is invalid through invalid form type"""
    def test_form_type_invalid(self):
        part_form = PartForm(
            {
                "piece": "Invalid",
                "part_number": "1",
                "pdf_file": SimpleUploadedFile(
                    "test.pdf", b"file_content", content_type="image/png"
                ),
            }
        )
        self.assertFalse(part_form.is_valid(), "Form is valid")

    """Tests to see if the form is invalid through missing fields"""
    def test_form_missing_fields(self):
        part_form = PartForm({})
        self.assertFormError(part_form, "instrument", "This field is required.")
        self.assertFormError(part_form, "part_number", "This field is required.")
        self.assertFormError(part_form, "pdf_file", "This field is required.")

        self.assertFalse(part_form.is_valid(), "Form is valid")


class TestSearchForm(TestCase):
    """Tests to see if the search form is valid"""
    def test_form_is_valid(self):
        search_form = SearchForm({"query": "Test Search"})
        self.assertTrue(search_form.is_valid(), "Form is not valid")

    """Tests to see if the form is invalid through invalid choice"""
    def test_form_is_invalid(self):
        search_form = SearchForm(
            {
                "filter": "Invalid Choice",
            }
        )
        self.assertFormError(
            search_form,
            "filter",
            "Select a valid choice. Invalid Choice is not one of the available choices.",
        )
        self.assertFalse(search_form.is_valid(), "Form is valid")
