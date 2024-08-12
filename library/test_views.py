from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
from .forms import PieceForm, PartForm, SearchForm
from .models import Piece, Part

#Library Views
class TestLibraryPrintView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword"
        )
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Test Band Arrangement",
        )
        self.piece.save()

    def test_library_print_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("library_print"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/library_print.html")
        self.assertIn(self.piece, response.context["pieces"])
        self.client.logout()


class TestPieceDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword")
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Test Band Arrangement",
        )
        self.piece.save()

    def test_piece_delete_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("library"),
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()

#Part Views
class TestPartView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpassword"
        )
        self.piece = Piece(
            title="Test Title",
            composer="Test Composer",
            arranged_by="Test Arranger",
            genre="Test Genre",
            mc_location="Test Location",
            band_arrangement="Test Band Arrangement",
        )
        self.piece.save()

        self.part = Part(
            piece=self.piece,
            instrument="Test Instrument",
            part_number=1,
            pdf_file=SimpleUploadedFile(
                "test.pdf", b"file_content", content_type="application/pdf"
            ),
        )
        self.part.save()

    def test_part_view_visible_pdf(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("part_view", args=[self.part.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/piece_view.html")
        self.assertEqual(self.part, response.context["part"])
        self.assertEqual(self.piece, response.context["piece"])
        self.assertIsInstance(response.context["part_form"], PartForm)
        self.client.logout()

    def test_part_view_upload_part(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("part_view", args=[self.part.id]),
            {
                "instrument": "Test Instrument",
                "part_number": 2,
                "pdf_file": SimpleUploadedFile(
                    "test.pdf", b"file_content", content_type="application/pdf"
                ),
            },
        )
        self.assertRedirects(
            response,
            reverse("part_view", args=[self.part.id]),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        part = Part.objects.get(pk=2)
        
        response = self.client.get(reverse("part_view", args=[self.part.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/piece_view.html")
        self.assertEqual(self.part, response.context["part"])
        self.assertEqual(self.piece, response.context["piece"])
        self.assertIn(part, response.context["piece"].parts.all())
        self.assertIsInstance(response.context["part_form"], PartForm)
        self.client.logout()
