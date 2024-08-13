from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
from .forms import PieceForm, PartForm, SearchForm
from .models import Piece, Part


# class TestLibraryPrintView(TestCase):
#     """Test the library print view and context"""

#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", email="test@test.com", password="testpassword"
#         )
#         self.piece = Piece(
#             title="Test Title",
#             composer="Test Composer",
#             arranged_by="Test Arranger",
#             genre="Test Genre",
#             mc_location="Test Location",
#             band_arrangement="Flexi-band",
#         )
#         self.piece.save()

#     def test_library_print_view(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.get(reverse("library_print"))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "library/library_print.html")
#         self.assertIn(self.piece, response.context["pieces"])
#         self.client.logout()

class TestPieceEditView(TestCase):
    """Test the piece edit view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword")
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Flexi-band",
        )
        self.piece.save()

    def test_piece_edit_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("piece_edit", args=[self.piece.id]),
            {
                "title": "Test Title Edited",
                "composer": "Test Composer Edited",
                "arranged_by": "Test Arranger Edited",
                "genre": "Test Genre Edited",
                "mc_location": "Test Location Edited",
                "band_arrangement": "Full-band",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.piece.refresh_from_db()
        self.assertEqual(self.piece.title, "Test Title Edited")
        self.assertEqual(self.piece.composer, "Test Composer Edited")
        self.assertEqual(self.piece.arranged_by, "Test Arranger Edited")
        self.assertEqual(self.piece.genre, "Test Genre Edited")
        self.assertEqual(self.piece.mc_location, "Test Location Edited")
        self.assertEqual(self.piece.band_arrangement, "Full-band")
        self.client.logout()

# class TestPieceDeleteView(TestCase):
#     """Test the piece delete view"""

#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", email="test@test.com", password="testpassword"
#         )
#         self.piece = Piece(
#             title="Test Title",
#             composer="Test Composer",
#             arranged_by="Test Arranger",
#             genre="Test Genre",
#             mc_location="Test Location",
#             band_arrangement="Flexi-band",
#         )
#         self.piece.save()

#     def test_piece_delete_view(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.post(
#             reverse("piece_delete", args=[self.piece.id]), follow=True
#         )
#         self.assertEqual(response.status_code, 200)
#         with self.assertRaises(Piece.DoesNotExist):
#             Piece.objects.get(pk=self.piece.id)
#         self.client.logout()
