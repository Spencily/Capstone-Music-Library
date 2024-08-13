from django.test import TestCase
from .forms import SetForm
from library.models import Piece


class TestSetForm(TestCase):
    """Creates a piece object to be used in the test form"""

    def setUp(self):
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Test Band Arrangement",
        )
        self.piece.save()

    def test_form_is_valid(self):
        """Tests to see if the set form is valid"""
        set_form = SetForm(
            {
                "title": "Test Title",
                "description": "Test Description",
                "pieces": (self.piece.id,),
            }
        )
        print(set_form.errors)
        self.assertTrue(set_form.is_valid(), "Form is not valid")

    def test_form_missing_fields(self):
        """Tests to see if the form is invalid through missing fields"""
        set_form = SetForm({})
        self.assertFormError(set_form, "title", "This field is required.")
        self.assertFormError(set_form, "pieces", "This field is required.")
        self.assertFalse(set_form.is_valid(), "Form is valid")
